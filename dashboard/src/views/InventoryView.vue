<script lang="ts" setup>
import type { Flower, Purchase } from '@/lib/types';
import { ref } from 'vue';
import { VueGoodTable } from 'vue-good-table-next';
import 'vue-good-table-next/dist/vue-good-table-next.css';

const columns = [
    {
        label: 'Artikelbezeichnung',
        field: 'product_id',
    },
    {
        label: 'Einkaufsdatum',
        field: 'date',
        type: 'date',
        formatFn: formatDate,
        html: true,
    },
    {
        label: 'Bunde',
        field: 'n_bunches',
        type: 'number',
        sortable: false,
        globalSearchDisabled: true,
    },
    {
        label: 'Stück',
        field: 'bunch_size',
        type: 'number',
        sortable: false,
        globalSearchDisabled: true,
    },
    {
        label: 'Menge',
        field: (rowObj: Purchase) => rowObj.n_bunches * rowObj.bunch_size,
        type: 'number',
        sortable: false,
        globalSearchDisabled: true,
    },
    {
        label: 'Preis',
        field: 'price',
        type: 'number',
        formatFn: formatCurrency,
    },
    {
        label: '%',
        field: "percentage",
        type: 'number',
        sortable: false,
        formatFn: formatPercentage,
        globalSearchDisabled: true,
    },
    {
        label: 'Summe',
        field: (rowObj: Purchase) => rowObj.n_bunches * rowObj.bunch_size * rowObj.price,
        type: 'number',
        formatFn: formatCurrency,
        globalSearchDisabled: true,
    }
];

const rows = [
    {
        product_id: 'R GR Mai Tai lang >>Rift<< 70 cm',
        date: "2024-07-01",
        n_bunches: 2,
        bunch_size: 50,
        price: 50,
        percentage: -10, children: [
            {
                product_id: 'R GR Mai Tai lang >>Rift<< 70 cm',
                date: "2024-07-01",
                n_bunches: 2,
                bunch_size: 50,
                price: 50,
                percentage: -10,
            },
            {
                product_id: 'R GR Mai Tai lang >>Rift<< 70 cm',
                date: "2024-02-11",
                n_bunches: 1,
                bunch_size: 50,
                price: 45,
                percentage: -11,
            },
            {
                product_id: 'R GR Mai Tai lang >>Rift<< 70 cm',
                date: "2023-12-21", n_bunches: 1, bunch_size: 50, price: 45, percentage: -4
            }
        ]
    },
    {
        product_id: 'WAXFL BL Me Gil 60g 80 cm',
        date: "2024-05-01",
        n_bunches: 2,
        bunch_size: 50,
        price: 70,
        percentage: -10
        , children: [
            {
                product_id: 'WAXFL BL Me Gil 60g 80 cm',
                date: "2024-05-01", n_bunches: 2, bunch_size: 50, price: 50, percentage: -10
            },
            { product_id: 'WAXFL BL Me Gil 60g 80 cm', date: "2024-02-11", n_bunches: 1, bunch_size: 50, price: 45, percentage: -11 },
        ]
    }
];

const inventory = ref<Flower[]>([]);

// onMounted(async () => {
//     inventory.value = await list_flowers();
// });

function formatCurrency(value: number) {
    return (value / 100).toLocaleString("de-DE", { style: "currency", currency: "EUR" });
}

function formatPercentage(value: number) {
    return value + ' %';
}

function formatDate(value: string): string {
    const date = new Date(value);
    return date.toLocaleDateString('de-DE', {
        day: '2-digit',
        month: 'short',
        year: 'numeric'
    });
}
</script>

<template>
    <div>
        <vue-good-table :columns="columns" :rows="rows" :enable-row-expand="true"
            :search-options="{ enabled: true, collapsible: true }" :pagination-options="{
                enabled: true,
                mode: 'pages',
                position: 'bottom',
                perPage: 3,
                dropdownAllowAll: true,
                nextLabel: 'Weiter',
                prevLabel: 'Zurück',
                rowsPerPageLabel: 'Anzahl pro Seite',
                ofLabel: 'von',
                pageLabel: 'Seite',
                allLabel: 'Alle',
            }" styleClass="vgt-table">
            <template #table-row="props">
                <span class="font-semibold">
                    <span v-if="props.column.field == 'date'" class="pi pi-circle-fill text-amber-300 pr-2"></span> {{
                        props.formattedRow[props.column.field] }}
                </span>
            </template>
            <template #row-details="props">
                <div class="fake-tr">
                    <template v-for="child in props.row.children" :key="child.product_id">
                        <div class="fake-td text-left">{{ child.product_id }}</div>
                        <div class="fake-td text-right">{{ formatDate(child.date) }}</div>
                        <div class="fake-td text-right">{{ child.n_bunches }}</div>
                        <div class="fake-td text-right">{{ child.bunch_size }}</div>
                        <div class="fake-td text-right">{{ child.n_bunches * child.bunch_size }}</div>
                        <div class="fake-td text-right">{{ formatCurrency(child.price) }}</div>
                        <div class="fake-td text-right">{{ formatPercentage(child.percentage) }}</div>
                        <div class="fake-td text-right">{{ formatCurrency(child.n_bunches * child.bunch_size *
                            child.price)
                        }}</div>
                    </template>
                </div>
                <div class="-mb-[.75em]">
                </div>
            </template>
        </vue-good-table>
    </div>
</template>

<style scoped>
.fake-tr {
    display: grid;
    grid-template-columns: repeat(2, auto) 92px 84px 94px 78px 65px 101px;
    margin: -.75em -.75em 0 -.75em;
}

.fake-td {
    padding: .75em .75em .75em .75em;
    vertical-align: top;
    border-bottom: 1px solid #e2e8f0;
}

.fake-td:nth-last-child(-n+8) {
    border-bottom: none;
}

.fake-td.text-left {
    padding-left: 1.5em;
}
</style>