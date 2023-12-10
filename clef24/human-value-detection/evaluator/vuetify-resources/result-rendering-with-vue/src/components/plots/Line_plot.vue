<template>
  <Line
    :options="{
      responsive: true, maintainAspectRatio: false,
      scales: {y: {min: 0, max: 1, offset: true}},
      plugins: {legend: {labels: {usePointStyle: true}}}
    }"
    :data="{labels: valueList, datasets: dataset}"
    class="line-plot"
  />
</template>

<script lang="ts">
import {Line} from "vue-chartjs";

const values: string[] = ['Self-Direction: thought', 'Self-Direction: action', 'Stimulation', 'Hedonism', 'Achievement', 'Power: dominance', 'Power: resources', 'Face', 'Security: personal', 'Security: societal', 'Tradition', 'Conformity: rules', 'Conformity: interpersonal', 'Humility', 'Benevolence: caring', 'Benevolence: dependability', 'Universalism: concern', 'Universalism: nature', 'Universalism: tolerance']

export default {
  name: 'value-line-plot',
  components: {Line},
  props: ['dataset'],
  data() {
    return {
      valueList: values
    }
  }
}
</script>
