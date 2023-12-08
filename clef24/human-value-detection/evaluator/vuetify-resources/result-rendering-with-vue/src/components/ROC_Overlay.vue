<template>
  <v-sheet ref="roc-overlay">
    <v-row>
      <v-col cols="7">
        <roc-main-plot
          :value-name="activeDataset.valueName"
          :value-label="activeDataset.valueLabel"
          :datasets="activeDataset.datasets"
          :auc="activeDataset.auc"
        />
      </v-col>
      <v-col cols="5">
        <v-container class="responsive-scroll-container">
          <v-row>
            <v-col xs="12" sm="6" lg="4" v-for="el in valueDatasets" :key="el.valueLabel">
              <value-roc-curve
                :value-name="el.valueName"
                :value-label="el.valueLabel"
                :datasets="el.datasets"
                :auc="el.auc"
                :ref="el.valueLabel"
                :active-label="activeLabel"
                @curveSelected="curveSelected"
              />
            </v-col>
          </v-row>
        </v-container>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<style>
.small-multiple {
  border-radius: 5pt;
}
.small-multiple:hover {
  background-color: rgb(240,240,240) !important;
}
.small-multiple.active {
  background-color: rgb(220,220,220) !important;
}

.responsive-scroll-container {
  overflow-y: auto;
  overflow-x: hidden;
  margin-top: auto;
  margin-bottom: auto;
}
.responsive-plot-aspect-ratio {
  width: 100% !important;
  height: 100% !important;
}

@media (max-width: 599.98px) {
  /* XS */
  .responsive-scroll-container {
    max-height: 300px !important;
  }
  .responsive-main-plot {
    width: 300px !important;
    height: 300px !important;
  }
  .responsive-sub-plot {
    width: 100px !important;
    height: 100px !important;
  }
}

@media (min-width: 600px) and (max-width: 959.98px) {
  /* SM */
  .responsive-scroll-container {
    max-height: 300px !important;
  }
  .responsive-main-plot {
    width: 300px !important;
    height: 300px !important;
  }
  .responsive-sub-plot {
    width: 100px !important;
    height: 100px !important;
  }
}

@media (min-width: 960px) and (max-width: 1279.98px) {
  /* MD */
  .responsive-scroll-container {
    max-height: 400px !important;
  }
  .responsive-main-plot {
    width: 400px !important;
    height: 400px !important;
  }
  .responsive-sub-plot {
    width: 100px !important;
    height: 100px !important;
  }
}

@media (min-width: 1280px) and (max-width: 1919.98px) {
  /* LG */
  .responsive-scroll-container {
    max-height: 600px !important;
  }
  .responsive-main-plot {
    width: 600px !important;
    height: 600px !important;
  }
  .responsive-sub-plot {
    width: 120px !important;
    height: 120px !important;
  }
}

@media (min-width: 1920px) and (max-width: 2559.98px) {
  /* XL */
  .responsive-scroll-container {
    max-height: 600px !important;
  }
  .responsive-main-plot {
    width: 600px !important;
    height: 600px !important;
  }
  .responsive-sub-plot {
    width: 120px !important;
    height: 120px !important;
  }
}

@media (min-width: 2560px) {
  /* XXL */
  .responsive-scroll-container {
    max-height: 1000px !important;
  }
  .responsive-main-plot {
    width: 1000px !important;
    height: 1000px !important;
  }
  .responsive-sub-plot {
    width: 150px !important;
    height: 150px !important;
  }
}

</style>

<script lang="ts">

import ValueRocCurve from "@/components/plots/Value_ROC_Curve.vue";
import RocMainPlot from "@/components/plots/ROC_main_plot.vue";
import {Scatter} from "vue-chartjs";

export default {
  name: 'roc-overlay',
  components: {Scatter, ValueRocCurve, RocMainPlot},
  props: ['allDatasets'],
  data () {
    return {
    }
  },
  setup (props) {
    const hiddenDataset = JSON.parse(JSON.stringify(props.allDatasets));
    Object.keys(hiddenDataset).forEach((valueLabel: string) => {
      hiddenDataset[valueLabel].borderColor = 'rgb(220,220,220)'
      hiddenDataset[valueLabel].backgroundColor = 'rgb(220,220,220)'
      hiddenDataset[valueLabel].fill = false
      hiddenDataset[valueLabel].pointRadius = 3
    });
    const finalDatasets: {valueName: string, valueLabel: string, datasets: any[], auc: string}[] = [];
    Object.keys(props.allDatasets).forEach((valueLabel: string) => {
      let newDataset = []
      newDataset.push(props.allDatasets[valueLabel])
      Object.keys(props.allDatasets).forEach((otherValueLabel: string) => {
        if (valueLabel !== otherValueLabel) {
          newDataset.push(hiddenDataset[otherValueLabel])
        }
      })
      finalDatasets.push({
        valueName: props.allDatasets[valueLabel].label,
        valueLabel,
        datasets: newDataset,
        auc: props.allDatasets[valueLabel].auc
      })
    });

    return {
      valueDatasets: finalDatasets,
      activeDataset: finalDatasets[0],
      activeLabel: finalDatasets[0].valueLabel
    }
  },
  methods: {
    curveSelected(selectedData: any) {
      this.activeDataset = selectedData;
      this.activeLabel = selectedData.valueLabel;
      (this.$refs['roc-overlay'] as any).$forceUpdate()
    }
  },
  mounted() {
    (this.$refs['roc-overlay'] as any).$forceUpdate()
  }
}
</script>
