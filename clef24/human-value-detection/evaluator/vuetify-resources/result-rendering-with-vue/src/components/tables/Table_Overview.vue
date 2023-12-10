<template>
  <!-- Type definition for data-table headers are currently not exported automatically -->
  <v-data-table
    id="overview-table"
    :headers="(dataHeaders as any)"
    :items="dataset"
  >
    <template v-slot:bottom></template>
  </v-data-table>
</template>

<style>
#overview-table tbody > tr > td:first-child {
  color: rgba(0, 0, 0, 0.6);
  font-weight: 500;
}
</style>

<script lang="ts">

export default {
  name: 'table-overview',
  props: ['dataset'],
  data () {
    return {
      dataHeaders: [
        { title: 'Metric', value: 'metric', align: "start", sortable: false },
        { title: 'Subtask 1', value: 'subtask1', align: "center", sortable: false },
        {
          title: 'Subtask 2', align: "center", sortable: false, children: [
            { title: 'attained', value: 'subtask2Attained', align: "center", sortable: false },
            { title: 'constrained', value: 'subtask2Constrained', align: "center", sortable: false },
            { title: 'overall', value: 'subtask2', align: "center", sortable: false },
          ]
        },
      ]
    }
  }
}

</script>
