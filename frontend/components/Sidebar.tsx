import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import HomeIcon from '@mui/icons-material/Home';
import CodeIcon from '@mui/icons-material/Code';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import SettingsIcon from '@mui/icons-material/Settings';
import SmartToyIcon from '@mui/icons-material/SmartToy';  // New import for Agents icon

const Sidebar: React.FC = () => {
  const router = useRouter();

  const isActive = (pathname: string) => router.pathname === pathname;

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: 240,
          boxSizing: 'border-box',
        },
      }}
    >
      <List>
        <ListItem button component={Link} href="/" selected={isActive('/')}>
          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          <ListItemText primary="Home" />
        </ListItem>
        <ListItem button component={Link} href="/ollama" selected={isActive('/ollama')}>
          <ListItemIcon>
            <CodeIcon />
          </ListItemIcon>
          <ListItemText primary="Ollama Interface" />
        </ListItem>
        <ListItem button component={Link} href="/health" selected={isActive('/health')}>
          <ListItemIcon>
            <HealthAndSafetyIcon />
          </ListItemIcon>
          <ListItemText primary="Health Status" />
        </ListItem>
        <ListItem button component={Link} href="/context" selected={isActive('/context')}>
          <ListItemIcon>
            <SettingsIcon />
          </ListItemIcon>
          <ListItemText primary="Context Management" />
        </ListItem>
        <ListItem button component={Link} href="/agents" selected={isActive('/agents')}>
          <ListItemIcon>
            <SmartToyIcon />
          </ListItemIcon>
          <ListItemText primary="Agents" />
        </ListItem>
      </List>
    </Drawer>
  );
};

export default Sidebar;
