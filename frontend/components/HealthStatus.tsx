import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styles from '@/styles/HealthStatus.module.css';

interface HealthStatus {
  database: {
    status: string;
    details: string | null;
  };
  elasticsearch: {
    status: string;
    details: {
      cluster_name: string;
      status: string;
      number_of_nodes: number;
      active_primary_shards: number;
    } | null;
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
    const interval = setInterval(fetchHealthStatus, 300000);

    return () => clearInterval(interval);
  }, []);

  if (loading) return <div className={styles.loading}>Loading health status...</div>;
  if (error) return <div className={styles.error}>Error: {error}</div>;
  if (!health) return null;

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>System Health</h2>
      <div className={styles.status}>
        <h3 className={styles.statusTitle}>Database</h3>
        <p className={styles[health.database.status]}>{health.database.status}</p>
        {health.database.status === 'initializing' ? (
          <p>Database is still initializing. Please wait...</p>
        ) : (
          <p>{health.database.details}</p>
        )}
      </div>
      <div className={styles.status}>
        <h3 className={styles.statusTitle}>Elasticsearch</h3>
        <p className={styles[health.elasticsearch.status]}>{health.elasticsearch.status}</p>
        {health.elasticsearch.details && (
          <ul className={styles.detailsList}>
            <li className={styles.detailsItem}>Cluster: {health.elasticsearch.details.cluster_name}</li>
            <li className={styles.detailsItem}>Status: {health.elasticsearch.details.status}</li>
            <li className={styles.detailsItem}>Nodes: {health.elasticsearch.details.number_of_nodes}</li>
            <li className={styles.detailsItem}>Shards: {health.elasticsearch.details.active_primary_shards}</li>
          </ul>
        )}
      </div>
    </div>
  );
};

export default HealthStatus;
