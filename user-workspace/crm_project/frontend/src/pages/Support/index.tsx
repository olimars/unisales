import { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  TextField,
  IconButton,
  Chip,
  Avatar,
  Tabs,
  Tab,
  Box,
} from '@mui/material';
import {
  Add as AddIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  Flag as FlagIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Schedule as ScheduleIcon,
} from '@mui/icons-material';

// Mock tickets data
const mockTickets = [
  {
    id: 1,
    subject: 'Cannot access dashboard',
    customer: 'John Doe',
    status: 'Open',
    priority: 'High',
    category: 'Technical',
    createdAt: '2024-02-20T10:30:00',
    lastUpdated: '2024-02-20T14:45:00',
  },
  {
    id: 2,
    subject: 'Billing inquiry',
    customer: 'Jane Smith',
    status: 'In Progress',
    priority: 'Medium',
    category: 'Billing',
    createdAt: '2024-02-19T15:20:00',
    lastUpdated: '2024-02-20T09:15:00',
  },
  {
    id: 3,
    subject: 'Feature request',
    customer: 'Mike Johnson',
    status: 'Closed',
    priority: 'Low',
    category: 'Feature Request',
    createdAt: '2024-02-18T11:00:00',
    lastUpdated: '2024-02-19T16:30:00',
  },
];

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const Support = () => {
  const [tickets, setTickets] = useState(mockTickets);
  const [searchTerm, setSearchTerm] = useState('');
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status.toLowerCase()) {
      case 'open':
        return <ErrorIcon className="text-red-500" />;
      case 'in progress':
        return <ScheduleIcon className="text-orange-500" />;
      case 'closed':
        return <CheckCircleIcon className="text-green-500" />;
      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Typography variant="h4" className="text-gray-800 font-medium">
          Support Tickets
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          className="bg-primary-600 hover:bg-primary-700"
        >
          New Ticket
        </Button>
      </div>

      {/* Ticket Statistics */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <Typography variant="h6">Total Tickets</Typography>
            <Typography variant="h3" className="mt-2">
              {tickets.length}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <Typography variant="h6">Open</Typography>
            <Typography variant="h3" className="mt-2">
              {tickets.filter(t => t.status === 'Open').length}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <Typography variant="h6">In Progress</Typography>
            <Typography variant="h3" className="mt-2">
              {tickets.filter(t => t.status === 'In Progress').length}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper className="p-4">
            <Typography variant="h6">Closed</Typography>
            <Typography variant="h3" className="mt-2">
              {tickets.filter(t => t.status === 'Closed').length}
            </Typography>
          </Paper>
        </Grid>
      </Grid>

      {/* Search and Filter */}
      <Paper className="p-4">
        <div className="flex gap-4">
          <TextField
            fullWidth
            variant="outlined"
            placeholder="Search tickets..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: <SearchIcon className="text-gray-400 mr-2" />,
            }}
          />
          <Button
            variant="outlined"
            startIcon={<FilterIcon />}
            className="min-w-[120px]"
          >
            Filter
          </Button>
        </div>

        {/* Tabs */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mt: 3 }}>
          <Tabs value={tabValue} onChange={handleTabChange}>
            <Tab label="All Tickets" />
            <Tab label="Open" />
            <Tab label="In Progress" />
            <Tab label="Closed" />
          </Tabs>
        </Box>

        {/* Tickets List */}
        <TabPanel value={tabValue} index={0}>
          <div className="space-y-4">
            {tickets.map(ticket => (
              <Card key={ticket.id} className="hover:shadow-md transition-shadow">
                <CardContent>
                  <div className="flex justify-between items-start">
                    <div className="flex items-center space-x-4">
                      <Avatar className="bg-primary-600">
                        {ticket.customer[0]}
                      </Avatar>
                      <div>
                        <Typography variant="h6">{ticket.subject}</Typography>
                        <Typography variant="body2" color="textSecondary">
                          {ticket.customer} - {ticket.category}
                        </Typography>
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <Chip
                        icon={<FlagIcon />}
                        label={ticket.priority}
                        size="small"
                        color={getPriorityColor(ticket.priority)}
                      />
                      <div className="flex items-center">
                        {getStatusIcon(ticket.status)}
                        <Typography variant="body2" className="ml-1">
                          {ticket.status}
                        </Typography>
                      </div>
                    </div>
                  </div>
                  <div className="mt-4 flex justify-between items-center text-sm text-gray-500">
                    <div>Created: {new Date(ticket.createdAt).toLocaleString()}</div>
                    <div>Last Updated: {new Date(ticket.lastUpdated).toLocaleString()}</div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </TabPanel>
        <TabPanel value={tabValue} index={1}>
          {/* Open Tickets */}
        </TabPanel>
        <TabPanel value={tabValue} index={2}>
          {/* In Progress Tickets */}
        </TabPanel>
        <TabPanel value={tabValue} index={3}>
          {/* Closed Tickets */}
        </TabPanel>
      </Paper>
    </div>
  );
};

export default Support;