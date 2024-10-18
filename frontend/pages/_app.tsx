import '@/styles/globals.css'
import type { AppProps } from 'next/app'
import Head from 'next/head'
import HealthStatus from '@/components/HealthStatus'
import styles from '@/styles/Layout.module.css'

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <div className={styles.container}>
      <Head>
        <title>AI-Enabled Agent Platform</title>
        <meta name="description" content="AI-Enabled Agent Platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className={styles.header}>
        <h1>AI-Enabled Agent Platform</h1>
      </header>

      <main className={styles.main}>
        <Component {...pageProps} />
      </main>

      <aside className={styles.healthStatus}>
        <HealthStatus />
      </aside>

      <footer className={styles.footer}>
        <p>&copy; 2024 Folsom-Point AI-Enabled Agent Platform</p>
      </footer>
    </div>
  )
}

export default MyApp
