import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, Grid, CircularProgress, Alert } from '@mui/material';
import StorageIcon from '@mui/icons-material/Storage';
import ElectricalServicesIcon from '@mui/icons-material/ElectricalServices';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

interface HealthStatus {
  database: {
    status: string;
    details: string;
  };
  elasticsearch: {
    status: string;
    details: {
      cluster_name: string;
      status: string;
      number_of_nodes: number;
      active_primary_shards: number;
    };
  };
}

const HealthStatus: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHealthStatus = async () => {
      try {
        const response = await axios.get<HealthStatus>(`${process.env.NEXT_PUBLIC_API_URL}/health/status`);
        setHealth(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch health status');
        setLoading(false);
      }
    };

    fetchHealthStatus();
    const interval = setInterval(fetchHealthStatus, 300000); // 5 minutes

    return () => clearInterval(interval);
  }, []);

  if (loading) return <CircularProgress />;
  if (error) return <Alert severity="error">{error}</Alert>;
  if (!health) return null;

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              <StorageIcon /> Database
            </Typography>
            <Typography color={health.database.status === 'connected' ? 'success.main' : 'error.main'}>
              {health.database.status === 'connected' ? (
                <CheckCircleOutlineIcon />
              ) : (
                <ErrorOutlineIcon />
              )}
              {health.database.status}
            </Typography>
            <Typography variant="body2">{health.database.details}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              <ElectricalServicesIcon /> Elasticsearch
            </Typography>
            <Typography color={health.elasticsearch.status === 'connected' ? 'success.main' : 'error.main'}>
              {health.elasticsearch.status === 'connected' ? (
                <CheckCircleOutlineIcon />
              ) : (
                <ErrorOutlineIcon />
              )}
              {health.elasticsearch.status}
            </Typography>
            <Typography variant="body2">Cluster: {health.elasticsearch.details.cluster_name}</Typography>
            <Typography variant="body2">Status: {health.elasticsearch.details.status}</Typography>
            <Typography variant="body2">Nodes: {health.elasticsearch.details.number_of_nodes}</Typography>
            <Typography variant="body2">Active Primary Shards: {health.elasticsearch.details.active_primary_shards}</Typography>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default HealthStatus;
