import { Grid, Card, CardContent, Typography } from '@mui/material';
import {
  TrendingUp,
  People,
  AttachMoney,
  Assignment
} from '@mui/icons-material';

const statsCards = [
  {
    title: 'Total Sales',
    value: '$24,500',
    icon: AttachMoney,
    color: 'text-green-600',
    bgColor: 'bg-green-100',
  },
  {
    title: 'Total Contacts',
    value: '1,250',
    icon: People,
    color: 'text-blue-600',
    bgColor: 'bg-blue-100',
  },
  {
    title: 'Active Deals',
    value: '45',
    icon: TrendingUp,
    color: 'text-purple-600',
    bgColor: 'bg-purple-100',
  },
  {
    title: 'Open Tasks',
    value: '28',
    icon: Assignment,
    color: 'text-orange-600',
    bgColor: 'bg-orange-100',
  },
];

const Dashboard = () => {
  return (
    <div className="space-y-6">
      <Typography variant="h4" className="text-gray-800 font-medium mb-6">
        Dashboard Overview
      </Typography>

      <Grid container spacing={3}>
        {statsCards.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <Grid item xs={12} sm={6} md={3} key={index}>
              <Card className="h-full">
                <CardContent className="flex items-center space-x-4">
                  <div className={`p-3 rounded-full ${stat.bgColor}`}>
                    <Icon className={`h-6 w-6 ${stat.color}`} />
                  </div>
                  <div>
                    <Typography color="textSecondary" gutterBottom>
                      {stat.title}
                    </Typography>
                    <Typography variant="h5" component="h2">
                      {stat.value}
                    </Typography>
                  </div>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <Grid container spacing={3} className="mt-6">
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" className="mb-4">
                Sales Overview
              </Typography>
              {/* Add Chart Component Here */}
              <div className="h-80 flex items-center justify-center bg-gray-50">
                Chart Placeholder
              </div>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" className="mb-4">
                Recent Activities
              </Typography>
              <div className="space-y-4">
                {[1, 2, 3, 4].map((_, index) => (
                  <div key={index} className="flex items-center space-x-3">
                    <div className="w-2 h-2 rounded-full bg-blue-500"></div>
                    <div>
                      <Typography variant="body2">
                        New contact added: John Doe
                      </Typography>
                      <Typography variant="caption" color="textSecondary">
                        2 hours ago
                      </Typography>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </div>
  );
};

export default Dashboard;