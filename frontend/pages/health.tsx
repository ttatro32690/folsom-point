import HealthStatus from '@/components/HealthStatus'
import styles from '@/styles/Home.module.css'

export default function Health() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>System Health</h1>
      <HealthStatus />
    </div>
  )
}
