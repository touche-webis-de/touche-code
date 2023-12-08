<template>
  <v-sheet
    v-bind:class="(activeLabel === valueLabel)?'pa-2 small-multiple active':'pa-2 small-multiple'"
    @click="handleClick()"
  >
    <v-row
      align="center"
      justify="center"
    >
      <v-col cols="12" align="center">
        {{valueName}}
        <div class="responsive-sub-plot">
          <Scatter
            :options="{
                  spanGaps: true,
                  animation: false,
                  responsive: true, maintainAspectRatio: false,
                  scales: {
                    x: {beginAtZero: true, min: 0, max: 1, offset: true, display: false},
                    y: {beginAtZero: true, min: 0, max: 1, offset: true, display: false}
                  },
                  elements: {line: {fill: true}},
                  plugins: {legend: {labels: {usePointStyle: true}, display: false}, tooltip: {enabled: false}}
                  }"
            :data="{datasets: datasets}"
            class="responsive-plot-aspect-ratio"
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
    name: "value-roc-curve",
    props: ["valueName", "valueLabel", "datasets", "auc", "activeLabel"],
    components: {Scatter},
    data () {
      return {
      }
    },
    methods: {
      handleClick() {
        this.$emit('curveSelected', {
          valueName: this.$props.valueName,
          valueLabel: this.$props.valueLabel,
          datasets: this.$props.datasets,
          auc: this.$props.auc,
        })
      }
    }
  }
</script>
