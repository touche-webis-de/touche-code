<template>
  <v-sheet class="ma-2 pa-2">
    <v-row
      align="center"
      justify="center"
    >
      <v-col cols="12" align="center">
        <h2>{{valueName}}</h2>
        <div class="responsive-main-plot">
          <Scatter
            :key="valueLabel"
            :options="{
                  responsive: true, maintainAspectRatio: false,
                  animation: false,
                  scales: {
                    x: {beginAtZero: true, min: 0, max: 1, offset: true, title: {display: true, text: 'FP-rate'}},
                    y: {beginAtZero: true, min: 0, max: 1, offset: true, title: {display: true, text: 'TP-rate'}}
                  },
                  elements: {line: {fill: true}},
                  plugins: {legend: {labels: {usePointStyle: true}, display: false}}
                  }"
            :data="{datasets: datasets}"
            style="width: 100% !important; height: 100% !important;"
          />
        </div>
        {{auc}}
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script lang="ts">
import {Scatter} from "vue-chartjs";

export default {
  name: 'roc-main-plot',
  components: {Scatter},
  props: ["valueName", "valueLabel", "datasets", "auc"]
}
</script>
