<script lang="ts" setup>
import { get_costs } from '@/lib/api';
import type { TotalCost } from '@/lib/types';
import { formatCurrency, formatDate, formatMonth, formatMonthShort } from '@/lib/utils';
import type { TooltipItem } from 'chart.js';
import Button from 'primevue/button';
import Chart from 'primevue/chart';
import DatePicker from 'primevue/datepicker';
import MeterGroup from 'primevue/metergroup';
import SelectButton from 'primevue/selectbutton';
import { computed, onMounted, ref } from 'vue';

const GROUP_OPTIONS = [
    { label: 'Tag', value: 'day' },
    { label: 'Monat', value: 'month' },
];


const totalCosts = ref<TotalCost[]>([])
const chartData = computed(() => {
    return {
        datasets: [
            {
                label: 'Exotic Garden',
                data: totalCosts.value,
            }
        ]
    };
});
const limit = ref<number>(5)
const costsByProduct = ref<TotalCost[]>([])
const metersData = computed(() => {
    const total = costsByProduct.value.reduce((acc, cost) => acc + cost.cost, 0);
    let top = 0;
    return [...costsByProduct.value.slice(0, limit.value).map((cost, index) => {
        const percentage = ((cost.cost / total) * 100);
        top += percentage;
        return {
            label: cost.group_by,
            value: percentage,
            color: `oklch(0.85 0.145 ${index * 50})`,
            text: formatCurrency(cost.cost)
        };
    }), {
        label: 'Sonstige',
        value: (100 - top),
        color: 'oklch(0.872 0.01 258.338)',
        text: formatCurrency(total / 100 * (100 - top))
    }];
});
const group_by = ref<string>("month")
const dates = ref<Date[]>([
    (() => {
        const d = new Date();
        d.setMonth(d.getMonth() - 5);
        d.setDate(1);
        return d;
    })(),
    new Date()
])

const chart_options = computed(() => {
    return {
        normalized: true,
        maintainAspectRatio: false,
        parsing: {
            xAxisKey: 'group_by',
            yAxisKey: 'cost'
        },
        plugins: {
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    title: (context: TooltipItem<'bar'>[]) => {
                        return group_by.value === "month" ? formatMonth(totalCosts.value[context[0].dataIndex].group_by) : formatDate(totalCosts.value[context[0].dataIndex].group_by);
                    },
                    label: (context: TooltipItem<'bar'>) => {
                        const label = context.dataset.label || '';
                        if (context.parsed.y !== null) {
                            return `${label}: ${formatCurrency(context.parsed.y)}`;
                        }
                        return label;
                    }
                }
            },
            legend: {
                labels: {
                    usePointStyle: true,
                },
            }
        },
        scales: {
            x: {
                stacked: true,
                ticks: {
                    callback: (index: number) => {
                        return group_by.value === "month" ?
                            formatMonthShort(totalCosts.value[index].group_by) : formatDate(totalCosts.value[index].group_by);
                    }
                },
            },
            y: {
                stacked: true,
                ticks: {
                    callback: (value: number) => {
                        return formatCurrency(value);
                    }
                },
            }
        }
    };
});

async function loadCosts() {
    if (!dates.value[0] || !dates.value[1]) return;
    totalCosts.value = await get_costs(group_by.value, dates.value[0].toISOString(), dates.value[1].toISOString())
}

async function loadProducts() {
    if (!dates.value[0] || !dates.value[1]) return;
    costsByProduct.value = await get_costs("product", dates.value[0].toISOString(), dates.value[1].toISOString())
}

async function loadAll() {
    await loadCosts()
    await loadProducts()
}


onMounted(async () => {
    await loadAll()
})
</script>

<template>
    <div class="min-w-full lg:min-w-2/3">
        <div class="mt-4 flex flex-wrap gap-6 items-center justify-between p-1">
            <SelectButton v-model="group_by" :options="GROUP_OPTIONS" option-label="label" option-value="value"
                :allow-empty="false" @change="loadCosts" />
            <DatePicker v-model="dates" selectionMode="range" :manualInput="false" showIcon iconDisplay="input"
                dateFormat="dd.mm.yy" :max-date="new Date()" @value-change="loadAll" />
        </div>
        <div class="flex flex-col gap-6 mt-6">
            <div class="w-full border border-surface rounded-2xl py-5 px-7 flex flex-col justify-between">
                <div class="flex-1 text-color font-semibold leading-6">Ausgaben</div>
                <Chart type="bar" :data="chartData" :options="chart_options" class="aspect-3/1" />
            </div>
            <div class="border border-surface rounded-2xl py-5 px-7 flex flex-col justify-between gap-6">
                <div class="flex-1 text-color font-semibold leading-6">Produkte</div>
                <MeterGroup :value="metersData" labelPosition="end">
                    <template #label="{ value }">
                        <div class="flex flex-col gap-6 mt-4">
                            <template v-for="val of value" :key="val.label">
                                <div class="flex items-center gap-2">
                                    <div class="w-2 h-2 rounded-full" :style="{ backgroundColor: val.color }">
                                    </div>
                                    <div class="text-color uppercase font-medium leading-6 flex-1">
                                        {{ val.label }}
                                        <span class="text-muted-color">({{ val.value.toFixed(1) }}%)</span>
                                    </div>
                                    <div class="leading-6 font-medium text-color">{{ val.text }}</div>
                                </div>
                            </template>
                        </div>
                    </template>
                </MeterGroup>
                <Button label="Show more" outlined @click="limit = Math.min(limit + 5, costsByProduct.length)" />
            </div>
        </div>
    </div>
</template>