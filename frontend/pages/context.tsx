import ContextManager from '@/components/ContextManager'
import styles from '@/styles/Home.module.css'

export default function Context() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Context Management</h1>
      <ContextManager />
    </div>
  )
}
