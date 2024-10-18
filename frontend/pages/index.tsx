import Head from 'next/head'
import styles from '@/styles/Home.module.css'

export default function Home() {
  return (
    <div className={styles.container}>
      <Head>
        <title>AI-Enabled Agent Platform</title>
        <meta name="description" content="AI-Enabled Agent Platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to the AI-Enabled Agent Platform
        </h1>

        <p className={styles.description}>
          Get started by editing{' '}
          <code className={styles.code}>pages/index.tsx</code>
        </p>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://github.com/yourusername/ai-agent-platform"
          target="_blank"
          rel="noopener noreferrer"
        >
          AI-Enabled Agent Platform
        </a>
      </footer>
    </div>
  )
}
