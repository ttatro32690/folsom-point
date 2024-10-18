import OllamaInterface from '@/components/OllamaInterface'
import styles from '@/styles/Home.module.css'

export default function Ollama() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Ollama Interface</h1>
      <OllamaInterface />
    </div>
  )
}
