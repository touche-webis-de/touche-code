<template>
  <!-- Type definition for data-table headers are currently not exported automatically -->
  <v-data-table
    v-model:items-per-page="itemsPerPage"
    :headers="(dataHeaders as any)"
    :items="tableData"
    item-key="id"
    @click:row="handleClick"
    id="sentence-table"
  >
    <template v-slot:top>
      <v-autocomplete
        v-model="selectedValue"
        :items="valueList"
        label="Select"
        single-line
      ></v-autocomplete>
    </template>
  </v-data-table>
</template>

<style>
#sentence-table tbody > tr > td:nth-child(3) {
  max-width: 250px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
#sentence-table thead > tr > th {
  white-space: nowrap;
}
#sentence-table thead > tr:nth-child(1) > th:nth-child(2),
#sentence-table thead > tr:nth-child(1) > th:nth-child(3),
#sentence-table thead > tr:nth-child(1) > th:nth-child(4),
/*#sentence-table thead > tr:nth-child(1) > th:nth-child(5),*/
/*#sentence-table thead > tr:nth-child(2) > th:nth-child(2),*/
#sentence-table thead > tr:nth-child(3) > th:nth-child(2),
#sentence-table thead > tr:nth-child(3) > th:nth-child(4),
/*#sentence-table thead > tr:nth-child(3) > th:nth-child(6),*/
#sentence-table tbody > tr > td:nth-child(2),
#sentence-table tbody > tr > td:nth-child(3) {
  border-right: thin solid rgba(var(--v-border-color), var(--v-border-opacity));
}
#sentence-table tbody tr:hover > td {
  background-color: rgb(220,220,220) !important;
}
#sentence-table tbody tr.active > td {
  background-color: rgb(180,180,180) !important;
}
</style>

<script lang="ts">

export default {
  name: 'table-sentence-data',
  props: ['valueList', 'tableData'],
  data() {
    return {
      itemsPerPage: 5,
      selectedValue: this.$props.valueList[0],
    }
  },
  methods: {
    handleClick (event: any, {item}: any) {
      // this.$emit('selectSentence', item.id)
    }
  },
  computed: {
    dataHeaders() {
      return [
        { title: 'Text-ID', align: 'start', sortable: true, key: 'Text-ID' },
        { title: 'Sentence-ID', align: 'start', sortable: true, key: 'Sentence-ID' },
        { title: 'Text', align: 'start', sortable: false, key: 'Text' },
        {
          title: 'Subtask 1', align: 'center', children: [
            { title: 'Delta', align: 'center', sortable: true, key: 'delta ' + this.selectedValue },
            { title: '| Delta |', align: 'center', sortable: true, key: 'deltaAbs ' + this.selectedValue },
          ]
        },
        {
          title: 'Subtask 2', align: 'center', children: [
            {
              title: 'attained', align: 'center', children: [
                { title: 'Delta', align: 'center', sortable: true, key: 'deltaAttained ' + this.selectedValue },
                { title: '| Delta |', align: 'center', sortable: true, key: 'deltaAbsAttained ' + this.selectedValue },
              ]
            },
            {
              title: 'constrained', align: 'center', children: [
                { title: 'Delta', align: 'center', sortable: true, key: 'deltaConstrained ' + this.selectedValue },
                { title: '| Delta |', align: 'center', sortable: true, key: 'deltaAbsConstrained ' + this.selectedValue },
              ]
            },
          ]
        }
      ]
    }
  }
}
</script>
