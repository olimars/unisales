import { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Button,
} from '@mui/material';
import {
  Download as DownloadIcon,
  TrendingUp,
  People,
  AttachMoney,
  Timeline,
} from '@mui/icons-material';

// Mock data for reports
const mockData = {
  salesOverview: {
    total: 125000,
    growth: 15,
    lastMonth: 25000,
    thisMonth: 28750,
  },
  customerMetrics: {
    total: 1250,
    new: 45,
    active: 890,
    churnRate: 2.5,
  },
  revenueMetrics: {
    mrr: 28750,
    arr: 345000,
    growth: 12,
  },
  topProducts: [
    { name: 'Product A', revenue: 45000, growth: 15 },
    { name: 'Product B', revenue: 32000, growth: 8 },
    { name: 'Product C', revenue: 28000, growth: 10 },
  ],
};

const Reports = () => {
  const [timeRange, setTimeRange] = useState('month');

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Typography variant="h4" className="text-gray-800 font-medium">
          Reports & Analytics
        </Typography>
        <div className="flex gap-4">
          <FormControl variant="outlined" size="small" className="min-w-[120px]">
            <InputLabel>Time Range</InputLabel>
            <Select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              label="Time Range"
            >
              <MenuItem value="week">This Week</MenuItem>
              <MenuItem value="month">This Month</MenuItem>
              <MenuItem value="quarter">This Quarter</MenuItem>
              <MenuItem value="year">This Year</MenuItem>
            </Select>
          </FormControl>
          <Button
            variant="outlined"
            startIcon={<DownloadIcon />}
            className="min-w-[120px]"
          >
            Export
          </Button>
        </div>
      </div>

      {/* Key Metrics */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-primary-100 rounded-full">
                <TrendingUp className="text-primary-600" />
              </div>
              <div>
                <Typography variant="body2" color="textSecondary">
                  Total Sales
                </Typography>
                <Typography variant="h5">
                  ${mockData.salesOverview.total.toLocaleString()}
                </Typography>
                <Typography variant="body2" className="text-green-600">
                  +{mockData.salesOverview.growth}% growth
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-full">
                <People className="text-blue-600" />
              </div>
              <div>
                <Typography variant="body2" color="textSecondary">
                  Total Customers
                </Typography>
                <Typography variant="h5">
                  {mockData.customerMetrics.total.toLocaleString()}
                </Typography>
                <Typography variant="body2" className="text-blue-600">
                  {mockData.customerMetrics.new} new this month
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-green-100 rounded-full">
                <AttachMoney className="text-green-600" />
              </div>
              <div>
                <Typography variant="body2" color="textSecondary">
                  Monthly Revenue
                </Typography>
                <Typography variant="h5">
                  ${mockData.revenueMetrics.mrr.toLocaleString()}
                </Typography>
                <Typography variant="body2" className="text-green-600">
                  +{mockData.revenueMetrics.growth}% from last month
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-purple-100 rounded-full">
                <Timeline className="text-purple-600" />
              </div>
              <div>
                <Typography variant="body2" color="textSecondary">
                  Churn Rate
                </Typography>
                <Typography variant="h5">
                  {mockData.customerMetrics.churnRate}%
                </Typography>
                <Typography variant="body2" className="text-purple-600">
                  {mockData.customerMetrics.active} active users
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
      </Grid>

      {/* Charts and Detailed Reports */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" className="mb-4">
                Sales Overview
              </Typography>
              <div className="h-80 flex items-center justify-center bg-gray-50">
                Sales Chart Placeholder
              </div>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" className="mb-4">
                Top Products
              </Typography>
              <div className="space-y-4">
                {mockData.topProducts.map((product, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div>
                      <Typography variant="body1">{product.name}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        ${product.revenue.toLocaleString()}
                      </Typography>
                    </div>
                    <Typography
                      variant="body2"
                      className={`${
                        product.growth > 0 ? 'text-green-600' : 'text-red-600'
                      }`}
                    >
                      {product.growth > 0 ? '+' : ''}{product.growth}%
                    </Typography>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" className="mb-4">
                Revenue Trends
              </Typography>
              <div className="h-80 flex items-center justify-center bg-gray-50">
                Revenue Chart Placeholder
              </div>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default Reports;