import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import styles from '@/styles/Sidebar.module.css';

const Sidebar: React.FC = () => {
  const router = useRouter();

  const isActive = (pathname: string) => router.pathname === pathname;

  return (
    <nav className={styles.sidebar}>
      <ul>
        <li className={isActive('/') ? styles.active : ''}>
          <Link href="/">Home</Link>
        </li>
        <li className={isActive('/ollama') ? styles.active : ''}>
          <Link href="/ollama">Ollama Interface</Link>
        </li>
        <li className={isActive('/health') ? styles.active : ''}>
          <Link href="/health">Health Status</Link>
        </li>
      </ul>
    </nav>
  );
};

export default Sidebar;
