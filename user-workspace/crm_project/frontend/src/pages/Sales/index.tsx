import { useState } from 'react';
import {
  Paper,
  Typography,
  Button,
  Card,
  CardContent,
  Chip,
  IconButton,
} from '@mui/material';
import {
  Add as AddIcon,
  MoreVert as MoreVertIcon,
  AttachMoney as MoneyIcon,
} from '@mui/icons-material';

// Define pipeline stages
const stages = [
  { id: 'lead', name: 'Lead', color: 'bg-gray-100' },
  { id: 'contact', name: 'Contact Made', color: 'bg-blue-100' },
  { id: 'proposal', name: 'Proposal', color: 'bg-yellow-100' },
  { id: 'negotiation', name: 'Negotiation', color: 'bg-orange-100' },
  { id: 'closed', name: 'Closed Won', color: 'bg-green-100' },
];

// Mock deals data
const mockDeals = [
  {
    id: 1,
    title: 'Enterprise Software Deal',
    company: 'Tech Corp',
    value: 50000,
    stage: 'lead',
    probability: 20,
  },
  {
    id: 2,
    title: 'Consulting Project',
    company: 'Consulting Co',
    value: 25000,
    stage: 'contact',
    probability: 40,
  },
  {
    id: 3,
    title: 'Software License',
    company: 'Software Inc',
    value: 75000,
    stage: 'proposal',
    probability: 60,
  },
  // Add more mock deals as needed
];

const Sales = () => {
  const [deals, setDeals] = useState(mockDeals);

  const getDealsInStage = (stageId: string) => {
    return deals.filter(deal => deal.stage === stageId);
  };

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
    }).format(value);
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Typography variant="h4" className="text-gray-800 font-medium">
          Sales Pipeline
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          className="bg-primary-600 hover:bg-primary-700"
        >
          Add Deal
        </Button>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4">
        {stages.map(stage => (
          <div key={stage.id} className="min-w-[300px]">
            <div className={`p-4 rounded-t-lg ${stage.color}`}>
              <div className="flex justify-between items-center">
                <Typography variant="h6" className="font-medium">
                  {stage.name}
                </Typography>
                <Typography variant="body2" className="text-gray-600">
                  {getDealsInStage(stage.id).length} Deals
                </Typography>
              </div>
            </div>
            
            <div className="space-y-3 p-3 bg-gray-50 rounded-b-lg min-h-[500px]">
              {getDealsInStage(stage.id).map(deal => (
                <Card key={deal.id} className="cursor-pointer hover:shadow-md transition-shadow">
                  <CardContent>
                    <div className="flex justify-between items-start">
                      <div>
                        <Typography variant="subtitle1" className="font-medium">
                          {deal.title}
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          {deal.company}
                        </Typography>
                      </div>
                      <IconButton size="small">
                        <MoreVertIcon />
                      </IconButton>
                    </div>
                    
                    <div className="mt-3 space-y-2">
                      <div className="flex items-center gap-2">
                        <MoneyIcon className="text-green-600" />
                        <Typography variant="body2" className="font-medium">
                          {formatCurrency(deal.value)}
                        </Typography>
                      </div>
                      
                      <Chip
                        label={`${deal.probability}% Probability`}
                        size="small"
                        className="bg-blue-100 text-blue-800"
                      />
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Sales;