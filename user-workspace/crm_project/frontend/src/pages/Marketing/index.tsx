import { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Add as AddIcon,
  MoreVert as MoreVertIcon,
  Email as EmailIcon,
  Campaign as CampaignIcon,
  Public as PublicIcon,
  Analytics as AnalyticsIcon,
  AttachMoney as AttachMoneyIcon,
} from '@mui/icons-material';

// Mock campaigns data
const mockCampaigns = [
  {
    id: 1,
    name: 'Spring Email Campaign',
    type: 'Email',
    status: 'Active',
    progress: 65,
    leads: 120,
    conversions: 45,
    budget: 5000,
    spent: 3250,
  },
  {
    id: 2,
    name: 'Social Media Promotion',
    type: 'Social',
    status: 'Planned',
    progress: 0,
    leads: 0,
    conversions: 0,
    budget: 3000,
    spent: 0,
  },
  {
    id: 3,
    name: 'Product Launch',
    type: 'Multi-channel',
    status: 'Completed',
    progress: 100,
    leads: 250,
    conversions: 85,
    budget: 10000,
    spent: 9800,
  },
];

const Marketing = () => {
  const [campaigns, setCampaigns] = useState(mockCampaigns);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [selectedCampaign, setSelectedCampaign] = useState<number | null>(null);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>, campaignId: number) => {
    setAnchorEl(event.currentTarget);
    setSelectedCampaign(campaignId);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
    setSelectedCampaign(null);
  };

  const getCampaignIcon = (type: string) => {
    switch (type) {
      case 'Email':
        return <EmailIcon />;
      case 'Social':
        return <PublicIcon />;
      default:
        return <CampaignIcon />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Active':
        return 'success';
      case 'Planned':
        return 'info';
      case 'Completed':
        return 'default';
      default:
        return 'default';
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Typography variant="h4" className="text-gray-800 font-medium">
          Marketing Campaigns
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          className="bg-primary-600 hover:bg-primary-700"
        >
          New Campaign
        </Button>
      </div>

      {/* Campaign Statistics */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <CampaignIcon className="text-primary-600" />
              <div>
                <Typography variant="body2" color="textSecondary">
                  Active Campaigns
                </Typography>
                <Typography variant="h6">
                  {campaigns.filter(c => c.status === 'Active').length}
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <AnalyticsIcon className="text-green-600" />
              <div>
                <Typography variant="body2" color="textSecondary">
                  Total Leads
                </Typography>
                <Typography variant="h6">
                  {campaigns.reduce((acc, curr) => acc + curr.leads, 0)}
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <PublicIcon className="text-blue-600" />
              <div>
                <Typography variant="body2" color="textSecondary">
                  Conversions
                </Typography>
                <Typography variant="h6">
                  {campaigns.reduce((acc, curr) => acc + curr.conversions, 0)}
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <div className="flex items-center space-x-3">
              <AttachMoneyIcon className="text-yellow-600" />
              <div>
                <Typography variant="body2" color="textSecondary">
                  Total Budget
                </Typography>
                <Typography variant="h6">
                  ${campaigns.reduce((acc, curr) => acc + curr.budget, 0).toLocaleString()}
                </Typography>
              </div>
            </div>
          </Paper>
        </Grid>
      </Grid>

      {/* Campaigns List */}
      <Grid container spacing={3}>
        {campaigns.map(campaign => (
          <Grid item xs={12} md={6} lg={4} key={campaign.id}>
            <Card>
              <CardContent>
                <div className="flex justify-between items-start">
                  <div className="flex items-center space-x-3">
                    {getCampaignIcon(campaign.type)}
                    <div>
                      <Typography variant="h6">{campaign.name}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        {campaign.type}
                      </Typography>
                    </div>
                  </div>
                  <div>
                    <IconButton
                      size="small"
                      onClick={(e) => handleMenuClick(e, campaign.id)}
                    >
                      <MoreVertIcon />
                    </IconButton>
                  </div>
                </div>

                <div className="mt-4">
                  <div className="flex justify-between items-center mb-2">
                    <Chip
                      label={campaign.status}
                      size="small"
                      color={getStatusColor(campaign.status)}
                    />
                    <Typography variant="body2">
                      {campaign.progress}% Complete
                    </Typography>
                  </div>
                  <LinearProgress
                    variant="determinate"
                    value={campaign.progress}
                    className="mb-4"
                  />

                  <Grid container spacing={2}>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="textSecondary">
                        Leads
                      </Typography>
                      <Typography variant="body1">{campaign.leads}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="textSecondary">
                        Conversions
                      </Typography>
                      <Typography variant="body1">{campaign.conversions}</Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="textSecondary">
                        Budget
                      </Typography>
                      <Typography variant="body1">
                        ${campaign.budget.toLocaleString()}
                      </Typography>
                    </Grid>
                    <Grid item xs={6}>
                      <Typography variant="body2" color="textSecondary">
                        Spent
                      </Typography>
                      <Typography variant="body1">
                        ${campaign.spent.toLocaleString()}
                      </Typography>
                    </Grid>
                  </Grid>
                </div>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={handleMenuClose}
      >
        <MenuItem onClick={handleMenuClose}>Edit Campaign</MenuItem>
        <MenuItem onClick={handleMenuClose}>View Details</MenuItem>
        <MenuItem onClick={handleMenuClose}>Duplicate</MenuItem>
        <MenuItem onClick={handleMenuClose} className="text-red-600">
          Delete
        </MenuItem>
      </Menu>
    </div>
  );
};

export default Marketing;