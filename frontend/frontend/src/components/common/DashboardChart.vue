<script setup>
import {
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  Chart,
  DoughnutController,
  Legend,
  LinearScale,
  Tooltip,
} from 'chart.js'
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

// Chart.js ships its chart controllers separately. Registering the elements alone
// leaves both `bar` and `doughnut` charts unable to render at runtime.
Chart.register(
  ArcElement,
  BarController,
  BarElement,
  CategoryScale,
  DoughnutController,
  Legend,
  LinearScale,
  Tooltip,
)

const props = defineProps({
  title: { type: String, required: true },
  labels: { type: Array, required: true },
  values: { type: Array, required: true },
  type: { type: String, default: 'doughnut' },
})

const canvas = ref(null)
let chart = null
const colors = ['#0d6efd', '#198754', '#ffc107', '#6f42c1', '#dc3545', '#0dcaf0', '#6c757d']
const render = () => {
  if (!canvas.value) return
  chart?.destroy()
  chart = new Chart(canvas.value, {
    type: props.type,
    data: { labels: props.labels, datasets: [{ data: props.values, backgroundColor: colors, borderWidth: 1 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: props.type === 'bar' ? 'top' : 'bottom' } },
      scales: props.type === 'bar' ? { y: { beginAtZero: true, ticks: { precision: 0 } } } : undefined,
    },
  })
}
onMounted(render)
watch(() => [props.labels, props.values, props.type], render, { deep: true })
onBeforeUnmount(() => chart?.destroy())
</script>

<template><div class="card h-100 shadow-sm"><div class="card-body"><h5>{{ title }}</h5><div v-if="!values.length" class="text-muted">No data available yet.</div><div v-else style="height: 280px"><canvas ref="canvas" :aria-label="title" role="img" /></div></div></div></template>
