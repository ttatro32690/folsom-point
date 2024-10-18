import styles from '@/styles/Home.module.css'
import OllamaInterface from '@/components/OllamaInterface'

export default function Home() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Welcome to the AI-Enabled Agent Platform</h1>
      <p className={styles.description}>
        Empowering AI agents with advanced capabilities
      </p>
      <OllamaInterface />
    </div>
  )
}
