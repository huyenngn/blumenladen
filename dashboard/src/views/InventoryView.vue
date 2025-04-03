<script lang="ts" setup>
import { get_flower, get_last_updated, list_flowers, update_flowers } from '@/lib/api';
import type { Flower } from '@/lib/types';
import { formatCurrency, formatDate, formatDateTime, formatPercentage } from '@/lib/utils';
import { Button } from 'primevue';
import ProgressSpinner from 'primevue/progressspinner';
import { onMounted, ref } from 'vue';
import { VueGoodTable } from 'vue-good-table-next';
import 'vue-good-table-next/dist/vue-good-table-next.css';

const columns = [
  {
    label: 'Artikelbezeichnung',
    field: 'product_id',
  },
  {
    label: 'Einkaufsdatum',
    field: (rowObj: Flower) => rowObj.purchases[0].date,
    type: 'date',
    formatFn: formatDate,
    html: true,
    globalSearchDisabled: true,
  },
  {
    label: 'Bunde',
    field: (rowObj: Flower) => rowObj.purchases[0].n_bunches,
    type: 'number',
    globalSearchDisabled: true,
  },
  {
    label: 'Stück',
    field: (rowObj: Flower) => rowObj.purchases[0].bunch_size,
    type: 'number',
    globalSearchDisabled: true,
  },
  {
    label: 'Menge',
    field: (rowObj: Flower) => rowObj.purchases[0].n_bunches * rowObj.purchases[0].bunch_size,
    type: 'number',
    globalSearchDisabled: true,
  },
  {
    label: 'Preis',
    field: (rowObj: Flower) => rowObj.purchases[0].price,
    type: 'number',
    formatFn: formatCurrency,
    gloablSearchDisabled: true,
  },
  {
    label: '%',
    field: (rowObj: Flower) => rowObj.purchases[0].percentage,
    type: 'number',
    formatFn: formatPercentage,
    globalSearchDisabled: true,
  },
  {
    label: 'Summe',
    field: (rowObj: Flower) =>
      rowObj.purchases[0].n_bunches * rowObj.purchases[0].bunch_size * rowObj.purchases[0].price,
    type: 'number',
    formatFn: formatCurrency,
    globalSearchDisabled: true,
  },
];

const SORT_OPTIONS = {
  enabled: false,
};

const PAGINATION_OPTIONS = {
  enabled: true,
  mode: 'pages',
  position: 'bottom',
  perPage: 10,
  dropdownAllowAll: false,
  nextLabel: 'Weiter',
  prevLabel: 'Zurück',
  rowsPerPageLabel: 'Anzahl pro Seite',
  ofLabel: 'von',
  pageLabel: 'Seite',
  allLabel: 'Alle',
};

const SEARCH_OPTIONS = {
  enabled: true,
  searchFn: searchTable,
  placeholder: 'Suche',
};

const inventory = ref<Flower[]>([]);
const lastUpdated = ref<string>('');
const updating = ref<boolean>(false);

async function updateInventory() {
  updating.value = true;
  const result = await update_flowers();
  if (result && 'date' in result) {
    lastUpdated.value = result.date;
    inventory.value = await list_flowers();
  }
  updating.value = false;
}

function searchTable(row: unknown, col: unknown, cellValue: string, searchTerm: string) {
  return cellValue.toLowerCase().includes(searchTerm.toLowerCase());
}

async function onRowExpand(params: {
  row: unknown;
  pageIndex: number;
  selected: boolean;
  event: Event;
}) {
  const flower = await get_flower((params.row as Flower).product_id);
  if (!flower) {
    return;
  }
  const idx = inventory.value.findIndex((el) => el.product_id === flower.product_id);
  inventory.value.splice(idx, 1, flower);
}

function getStatusClass(row: Flower) {
  const amount = row.purchases[0].n_bunches * row.purchases[0].bunch_size;
  const daysSincePurchase = Math.floor(
    (new Date().getTime() - new Date(row.purchases[0].date).getTime()) / (1000 * 60 * 60 * 24),
  );
  const factor = amount / daysSincePurchase;
  if (factor < 10) {
    return 'text-red-300';
  }
  if (factor < 16) {
    return 'text-amber-300';
  }
  return 'text-green-300';
}

onMounted(async () => {
  await get_last_updated().then((result) => {
    if (result && 'date' in result) {
      lastUpdated.value = result.date;
    }
  });
  await updateInventory();
});
</script>

<template>
  <div>
    <div class="flex items-end justify-between pb-2">
      <span>Letzter Stand: {{ formatDateTime(lastUpdated) }}</span>
      <div class="flex items-center">
        <ProgressSpinner
          v-if="updating"
          stroke-width="8"
          class="mr-2 h-6 w-6"
          fill="transparent"
          aria-label="Loading"
        />
        <Button
          label="Neu laden"
          icon="pi pi-refresh"
          class="p-button-sm"
          severity="secondary"
          @click="updateInventory"
          :disabled="updating"
        />
      </div>
    </div>
    <vue-good-table
      :columns="columns"
      :rows="inventory"
      max-height="calc(100dvh - 265px)"
      :fixed-header="true"
      :sort-options="SORT_OPTIONS"
      :enable-row-expand="true"
      :search-options="SEARCH_OPTIONS"
      :pagination-options="PAGINATION_OPTIONS"
      @row-click="onRowExpand"
      styleClass="vgt-table"
    >
      <template #table-row="props">
        <span class="font-semibold">
          <span
            v-if="props.column.label == 'Einkaufsdatum'"
            :class="['pi pi-circle-fill pr-2', getStatusClass(props.row)]"
          ></span>
          {{ props.formattedRow[props.column.field] }}
        </span>
      </template>
      <template #row-details="props">
        <div class="fake-tr">
          <template v-for="child in props.row.purchases" :key="child.product_id">
            <div class="fake-td text-left">{{ child.product_id }}</div>
            <div
              v-for="col in [
                formatDate(child.date),
                child.n_bunches,
                child.bunch_size,
                child.n_bunches * child.bunch_size,
                formatCurrency(child.price),
                formatPercentage(child.percentage),
                formatCurrency(child.n_bunches * child.bunch_size * child.price),
              ]"
              :key="col"
              class="fake-td text-right"
            >
              {{ col }}
            </div>
          </template>
        </div>
        <div class="-mb-[.75em]"></div>
      </template>
    </vue-good-table>
  </div>
</template>

<style scoped>
.fake-tr {
  display: grid;
  grid-template-columns: auto 166px 92px 84px 94px 78px 65px 101px;
  margin: -0.75em -0.75em 0 -0.75em;
}

.fake-td {
  padding: 0.75em 0.75em 0.75em 0.75em;
  vertical-align: top;
  border-bottom: 1px solid #e2e8f0;
}

.fake-td:nth-last-child(-n + 8) {
  border-bottom: none;
}

.fake-td.text-left {
  padding-left: 1.5em;
}
</style>
