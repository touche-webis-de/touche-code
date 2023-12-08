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
    <template v-slot:body="{ items }">
      <tr v-for="(item, index) in (items as any[])" :key="index" class="v-data-table__tr v-data-table__tr--clickable" @click="handleClick($event, {item})">
        <td class="v-data-table__td v-data-table-column--align-start">{{item['Text-ID']}}</td>
        <td class="v-data-table__td v-data-table-column--align-start">{{item['Sentence-ID']}}</td>
        <td class="v-data-table__td v-data-table-column--align-start">{{item['Text']}}</td>
        <td class="v-data-table__td v-data-table-column--align-center" :style="applyGradient(item['delta ' + selectedValue])">{{item['delta ' + selectedValue]}}</td>
        <td class="v-data-table__td v-data-table-column--align-center" :style="applyGradient(item['deltaAbs ' + selectedValue])">{{item['deltaAbs ' + selectedValue]}}</td>
        <td class="v-data-table__td v-data-table-column--align-center" :style="applyGradient(item['deltaAttained ' + selectedValue])">{{item['deltaAttained ' + selectedValue]}}</td>
        <td class="v-data-table__td v-data-table-column--align-center" :style="applyGradient(item['deltaAbsAttained ' + selectedValue])">{{item['deltaAbsAttained ' + selectedValue]}}</td>
        <td class="v-data-table__td v-data-table-column--align-center" :style="applyGradient(item['deltaConstrained ' + selectedValue])">{{item['deltaConstrained ' + selectedValue]}}</td>
        <td class="v-data-table__td v-data-table-column--align-center" :style="applyGradient(item['deltaAbsConstrained ' + selectedValue])">{{item['deltaAbsConstrained ' + selectedValue]}}</td>
      </tr>
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
    },
    applyGradient(value: number) {
      return "background-color: rgba(255,0,0," + Math.abs(value) + ") !important;"
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
