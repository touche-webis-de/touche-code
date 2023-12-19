<template>
  <v-app>
    <v-main class="overflow-x-hidden overflow-y-auto">
      <v-container>
        <v-row style="margin-top: 20px; margin-bottom: 20px;">
          <v-col cols="12" lg="12">
            <h2>ValueEval'24 Run Analysis</h2>
          </v-col>
          <v-col cols="12" lg="12">
            <div class="panel margin-panel">
              <div class="panel-heading">Overview</div>
              <div class="panel-body">
                <p>
                  All metrics are macro-averaged over values except for Subtask 2 overall, which are instead micro-averages of attained and constrained.
                </p>
                <table-overview :dataset="generalData" />
              </div>
            </div>
          </v-col>
        </v-row>
        <div class="panel">
          <div class="panel-heading">Roc Curves</div>
          <div class="panel-body">
            <p>
              The blue circle marks the performance at confidence threshold 0.5 as used in the overview.
            </p>
            <v-expansion-panels>
              <v-expansion-panel>
                <v-expansion-panel-title>ROC-Curve Subtask 1</v-expansion-panel-title>
                <v-expansion-panel-text>
                  <roc-overlay v-bind:all-datasets="valueRocCurve[0]"/>
                </v-expansion-panel-text>
              </v-expansion-panel>
              <v-expansion-panel>
                <v-expansion-panel-title>ROC-Curve Subtask 2 attained</v-expansion-panel-title>
                <v-expansion-panel-text>
                  <roc-overlay v-bind:all-datasets="valueRocCurve[1]"/>
                </v-expansion-panel-text>
              </v-expansion-panel>
              <v-expansion-panel>
                <v-expansion-panel-title>ROC-Curve Subtask 2 constrained</v-expansion-panel-title>
                <v-expansion-panel-text>
                  <roc-overlay v-bind:all-datasets="valueRocCurve[2]"/>
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </div>
        </div>
        <v-row style="margin-top: 20px; margin-bottom: 20px;">
          <v-col cols="12" lg="6">
            <div class="panel">
              <div class="panel-heading">Value-wise Metrics for Subtask 1</div>
              <div class="panel-body">
                <v-row
                  align="center"
                  justify="center"
                >
                  <h2>F1-Score</h2>
                  <v-col cols="12">
                    <value-line-plot :dataset="linePlotData.subtask1.plot1"/>
                  </v-col>
                  <h2>Precision & Recall</h2>
                  <v-col cols="12">
                    <value-line-plot :dataset="linePlotData.subtask1.plot2"/>
                  </v-col>
                </v-row>
              </div>
            </div>
          </v-col>
          <v-col cols="12" lg="6">
            <div class="panel">
              <div class="panel-heading">Value-wise Metrics for Subtask 2</div>
              <div class="panel-body">
                <v-row
                  align="center"
                  justify="center"
                >
                  <h2>F1-Score</h2>
                  <v-col cols="12">
                    <value-line-plot :dataset="linePlotData.subtask2.plot1"/>
                  </v-col>
                  <h2>Precision & Recall</h2>
                  <v-col cols="12">
                    <value-line-plot :dataset="linePlotData.subtask2.plot2"/>
                  </v-col>
                </v-row>
              </div>
            </div>
          </v-col>
        </v-row>
        <div class="panel margin-panel" style="min-height: 532px">
          <div class="panel-heading">
            Details
          </div>
          <div class="panel-body panel-body-no-bottom-pad">
            <p>
              Delta is the prediction confidence minus the ground truth: Delta &lt; -0.5 for false negatives; Delta &gt; 0.5 for false positives.
            </p>
            <table-sentence-data
              :value-list="sentenceValues"
              :table-data="sentenceTableData"
            />
          </div>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<style>
  .panel {
    border: 1px solid #337ab7;
    border-radius: 4px;
    box-shadow: 0 1px 1px rgba(0,0,0,.05);
    display: flex;
    flex-direction: column;
  }
  .panel.margin-panel {
    margin-bottom: 20px;
  }
  .panel > .panel-heading {
    flex-shrink: 0;
    color: #fff;
    background-color: #337ab7;
    border-color: #337ab7;
    padding: 10px 15px;
    border-bottom: 1px solid #337ab7;
    border-top-left-radius: 3px;
    border-top-right-radius: 3px;
  }
  .panel > .panel-body {
    padding: 15px 15px 15px 15px;
    flex-grow: 1;
  }
  .panel > .panel-body.panel-body-no-bottom-pad {
    padding-bottom: 0;
  }

  .line-plot {
    min-height: 300px;
    max-height: 450px;
  }

  @media (max-width: 599.98px) {
    /* XS */
    html {
      font-size: 0.5rem !important;
    }
  }
  @media (min-width: 600px) and (max-width: 959.98px) {
    /* SM */
    html {
      font-size: 0.6rem !important;
    }
  }
  @media (min-width: 960px) and (max-width: 1279.98px) {
    /* MD */
    html {
      font-size: 0.7rem !important;
    }
  }
  @media (min-width: 1280px) and (max-width: 1919.98px) {
    /* LG */
    html {
      font-size: 0.85rem !important;
    }
  }
</style>

<script lang="ts">
  import ValueContinuum from "@/components/continuum/Continuum.vue";
  import MetricContinuum from "@/components/continuum/Continuum_Metrics.vue";

  import RocOverlay from '@/components/ROC_Overlay.vue';

  import TableOverview from "@/components/tables/Table_Overview.vue";
  import TableSentenceData from "@/components/tables/Table_Sentence_Data.vue";
  import ValueLinePlot from "@/components/plots/Line_plot.vue";

  export default {
    name: "app",
    components: {
      ValueLinePlot, TableSentenceData, TableOverview, RocOverlay, ValueContinuum, MetricContinuum
    },
    setup () {
      const generalData = (window as any)['general_data']();

      const valueRocCurve = (window as any)['value_roc_curve']();

      const linePlotData = (window as any)['line_plot_data']();

      const sentenceData = (window as any)['sentence_data']();

      return {
        generalData,
        valueRocCurve,
        linePlotData,
        sentenceValues: sentenceData.values,
        sentenceTableData: sentenceData.tableData
      }
    }
  }
</script>
