import { useState } from 'react';
import {
  Grid,
  Paper,
  Typography,
  Tabs,
  Tab,
  Box,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
} from '@mui/material';
import {
  Save as SaveIcon,
  Notifications as NotificationsIcon,
  Security as SecurityIcon,
  Business as BusinessIcon,
  Email as EmailIcon,
  Extension as ExtensionIcon,
} from '@mui/icons-material';

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
      id={`settings-tabpanel-${index}`}
      aria-labelledby={`settings-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
};

const Settings = () => {
  const [tabValue, setTabValue] = useState(0);
  const [settings, setSettings] = useState({
    companyName: 'Acme Corp',
    email: 'admin@acmecorp.com',
    phone: '+1 234 567 890',
    address: '123 Business Street',
    emailNotifications: true,
    pushNotifications: true,
    twoFactorAuth: false,
    darkMode: false,
  });

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleSettingChange = (setting: string, value: string | boolean) => {
    setSettings(prev => ({
      ...prev,
      [setting]: value,
    }));
  };

  return (
    <div className="space-y-6">
      <Typography variant="h4" className="text-gray-800 font-medium">
        Settings
      </Typography>

      <Paper>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          variant="scrollable"
          scrollButtons="auto"
          className="border-b border-gray-200"
        >
          <Tab icon={<BusinessIcon />} label="Company" />
          <Tab icon={<NotificationsIcon />} label="Notifications" />
          <Tab icon={<SecurityIcon />} label="Security" />
          <Tab icon={<EmailIcon />} label="Email" />
          <Tab icon={<ExtensionIcon />} label="Integrations" />
        </Tabs>

        {/* Company Settings */}
        <TabPanel value={tabValue} index={0}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <div className="space-y-4">
                <TextField
                  fullWidth
                  label="Company Name"
                  value={settings.companyName}
                  onChange={(e) => handleSettingChange('companyName', e.target.value)}
                />
                <TextField
                  fullWidth
                  label="Email"
                  value={settings.email}
                  onChange={(e) => handleSettingChange('email', e.target.value)}
                />
                <TextField
                  fullWidth
                  label="Phone"
                  value={settings.phone}
                  onChange={(e) => handleSettingChange('phone', e.target.value)}
                />
                <TextField
                  fullWidth
                  label="Address"
                  multiline
                  rows={3}
                  value={settings.address}
                  onChange={(e) => handleSettingChange('address', e.target.value)}
                />
                <Button
                  variant="contained"
                  startIcon={<SaveIcon />}
                  className="bg-primary-600 hover:bg-primary-700"
                >
                  Save Changes
                </Button>
              </div>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Notifications Settings */}
        <TabPanel value={tabValue} index={1}>
          <List>
            <ListItem>
              <ListItemText
                primary="Email Notifications"
                secondary="Receive email notifications for important updates"
              />
              <ListItemSecondaryAction>
                <Switch
                  checked={settings.emailNotifications}
                  onChange={(e) => handleSettingChange('emailNotifications', e.target.checked)}
                />
              </ListItemSecondaryAction>
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemText
                primary="Push Notifications"
                secondary="Receive push notifications in your browser"
              />
              <ListItemSecondaryAction>
                <Switch
                  checked={settings.pushNotifications}
                  onChange={(e) => handleSettingChange('pushNotifications', e.target.checked)}
                />
              </ListItemSecondaryAction>
            </ListItem>
          </List>
        </TabPanel>

        {/* Security Settings */}
        <TabPanel value={tabValue} index={2}>
          <List>
            <ListItem>
              <ListItemText
                primary="Two-Factor Authentication"
                secondary="Add an extra layer of security to your account"
              />
              <ListItemSecondaryAction>
                <Switch
                  checked={settings.twoFactorAuth}
                  onChange={(e) => handleSettingChange('twoFactorAuth', e.target.checked)}
                />
              </ListItemSecondaryAction>
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemText
                primary="Change Password"
                secondary="Update your account password"
              />
              <ListItemSecondaryAction>
                <Button variant="outlined" size="small">
                  Change
                </Button>
              </ListItemSecondaryAction>
            </ListItem>
          </List>
        </TabPanel>

        {/* Email Settings */}
        <TabPanel value={tabValue} index={3}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <div className="space-y-4">
                <TextField
                  fullWidth
                  label="SMTP Host"
                  placeholder="smtp.example.com"
                />
                <TextField
                  fullWidth
                  label="SMTP Port"
                  placeholder="587"
                />
                <TextField
                  fullWidth
                  label="Username"
                  placeholder="your-email@example.com"
                />
                <TextField
                  fullWidth
                  type="password"
                  label="Password"
                  placeholder="••••••••"
                />
                <Button
                  variant="contained"
                  startIcon={<SaveIcon />}
                  className="bg-primary-600 hover:bg-primary-700"
                >
                  Save Email Settings
                </Button>
              </div>
            </Grid>
          </Grid>
        </TabPanel>

        {/* Integrations Settings */}
        <TabPanel value={tabValue} index={4}>
          <List>
            <ListItem>
              <ListItemText
                primary="Slack Integration"
                secondary="Connect your Slack workspace"
              />
              <ListItemSecondaryAction>
                <Button variant="outlined" size="small">
                  Connect
                </Button>
              </ListItemSecondaryAction>
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemText
                primary="Google Calendar"
                secondary="Sync with Google Calendar"
              />
              <ListItemSecondaryAction>
                <Button variant="outlined" size="small">
                  Connect
                </Button>
              </ListItemSecondaryAction>
            </ListItem>
            <Divider />
            <ListItem>
              <ListItemText
                primary="Zapier"
                secondary="Connect with Zapier for automation"
              />
              <ListItemSecondaryAction>
                <Button variant="outlined" size="small">
                  Connect
                </Button>
              </ListItemSecondaryAction>
            </ListItem>
          </List>
        </TabPanel>
      </Paper>
    </div>
  );
};

export default Settings;