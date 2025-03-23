from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from django.db import connection
from .models import Dashboard, Widget, Report, ReportExport, Metric
from .serializers import (
    DashboardSerializer,
    DashboardListSerializer,
    WidgetSerializer,
    ReportSerializer,
    ReportListSerializer,
    ReportExportSerializer,
    MetricSerializer
)

class DashboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing dashboards.
    """
    permission_classes = [IsAuthenticated]
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return DashboardListSerializer
        return DashboardSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only their dashboards and public ones
        if not user.is_staff:
            queryset = queryset.filter(
                Q(created_by=user) | Q(is_public=True)
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def duplicate(self, request, pk=None):
        """
        Duplicate a dashboard with all its widgets.
        """
        dashboard = self.get_object()
        new_dashboard = Dashboard.objects.create(
            name=f"Copy of {dashboard.name}",
            description=dashboard.description,
            created_by=request.user,
            is_public=False
        )

        # Duplicate widgets
        for widget in dashboard.widgets.all():
            Widget.objects.create(
                dashboard=new_dashboard,
                name=widget.name,
                widget_type=widget.widget_type,
                query=widget.query,
                refresh_interval=widget.refresh_interval,
                position_x=widget.position_x,
                position_y=widget.position_y,
                width=widget.width,
                height=widget.height,
                configuration=widget.configuration
            )

        serializer = self.get_serializer(new_dashboard)
        return Response(serializer.data)

class WidgetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing dashboard widgets.
    """
    permission_classes = [IsAuthenticated]
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['dashboard', 'widget_type']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only widgets from their dashboards and public ones
        if not user.is_staff:
            queryset = queryset.filter(
                Q(dashboard__created_by=user) | Q(dashboard__is_public=True)
            )

        return queryset

    @action(detail=True, methods=['post'])
    def execute_query(self, request, pk=None):
        """
        Execute the widget's query and return results.
        """
        widget = self.get_object()
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(widget.query)
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            return Response({
                'columns': columns,
                'data': results
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class ReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing reports.
    """
    permission_classes = [IsAuthenticated]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['report_type', 'is_scheduled', 'schedule_type']
    search_fields = ['name', 'description']

    def get_serializer_class(self):
        if self.action == 'list':
            return ReportListSerializer
        return ReportSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user

        # If user is not admin, show only their reports
        if not user.is_staff:
            queryset = queryset.filter(
                Q(created_by=user) | Q(recipients=user)
            ).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def generate(self, request, pk=None):
        """
        Generate and export a report.
        """
        report = self.get_object()
        export_format = request.data.get('format', 'csv')
        
        try:
            # Execute report query
            with connection.cursor() as cursor:
                cursor.execute(report.query)
                columns = [col[0] for col in cursor.description]
                results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            # Create export record
            export = ReportExport.objects.create(
                report=report,
                format=export_format,
                created_by=request.user
            )
            
            # Here you would typically generate the file based on format
            # and attach it to the export record
            
            report.last_run = timezone.now()
            report.save()
            
            return Response({
                'export': ReportExportSerializer(export).data,
                'columns': columns,
                'data': results
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class MetricViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing metrics.
    """
    permission_classes = [IsAuthenticated]
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['content_type', 'timestamp']
    ordering_fields = ['timestamp', 'value']
    ordering = ['-timestamp']

    @action(detail=False, methods=['get'])
    def trends(self, request):
        """
        Get metric trends over time.
        """
        metric_name = request.query_params.get('name')
        days = int(request.query_params.get('days', 30))
        
        if not metric_name:
            return Response(
                {'error': 'Metric name is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        start_date = timezone.now() - timezone.timedelta(days=days)
        metrics = self.get_queryset().filter(
            name=metric_name,
            timestamp__gte=start_date
        ).order_by('timestamp')
        
        data = [{
            'timestamp': metric.timestamp,
            'value': metric.value
        } for metric in metrics]
        
        return Response(data)
