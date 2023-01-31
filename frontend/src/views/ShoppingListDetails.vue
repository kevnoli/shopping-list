<template>
  <v-card>
    <v-card-text>
      <div class="d-flex align-center">
        <h2 v-if="!editing">{{ list.name }}</h2>
        <v-text-field v-else v-model="list.name" variant="underlined" hide-details />
        <v-spacer />
        <v-btn @click="productDialog = true" icon="mdi-cart-plus" variant="flat" />
        <v-btn @click="toggleEditing" :icon="editing ? 'mdi-check' : 'mdi-pencil'" variant="flat"></v-btn>
      </div>
      <div class="d-flex my-4">
        <v-spacer></v-spacer>
        <h2>$ {{ list_total }}</h2>
      </div>
      <product-search v-model="productDialog" @selected="itemSelected" />
      <v-data-table :headers="headers" :search="search" :custom-filter="itemFilter" :items="products" dense>
        <template #top>
          <v-text-field v-model="search" label="Search" density="compact" variant="solo" single-line clearable />
        </template>
        <template #item.price="{ item }">
          <v-currency-input v-model="item.value.price"
            @change="handleChange(item.value.product.id, 'price', item.value.price)" prefix="$" class="pb-3"
            density="compact" variant="plain" single-line hide-details :readonly="item.value.finished" />
        </template>
        <template #item.amount_to_buy="{ item }">
          <v-text-field v-model="item.value.amount_to_buy"
            @change="handleChange(item.value.product.id, 'amount_to_buy', item.value.amount_to_buy)" class="pb-3"
            density="compact" variant="plain" single-line hide-details :readonly="item.value.finished" />
        </template>
        <template #item.match="{ item }">
          <v-btn flat size="small" icon="mdi-link" @click="matchAmounts(item)" />
        </template>
        <template #item.amount_bought="{ item }">
          <v-text-field :id="`bought_${item.value.product.id}`" v-model="item.value.amount_bought"
            @change="handleChange(item.value.product.id, 'amount_bought', item.value.amount_bought)" class="pb-3"
            density="compact" variant="plain" single-line hide-details :readonly="item.value.finished" />
        </template>
        <template #item.total="{ item }">
          <v-text-field
            :model-value="Intl.NumberFormat('en-US', { minimumFractionDigits: 2 }).format(item.raw.price * item.raw.amount_bought)"
            prefix="$" class="pb-3" density="compact" variant="plain" single-line hide-details readonly />
        </template>
        <template #item.actions="{ item }">
          <v-btn flat size="small" :icon="item.value.finished ? 'mdi-pencil' : 'mdi-check'"
            @click="item.value.finished = !item.value.finished" />
          <v-btn flat size="small" icon="mdi-delete" @click.prevent="deleteItem(item)" />
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { inject, onMounted, ref, watch, computed } from "vue";
import { useRoute } from 'vue-router';

import ProductSearch from "@/components/ProductSearch.vue";

const route = useRoute()
const axios = inject("axios")

const productDialog = ref(false)
const list = ref({})
const products = ref([])
const search = ref("")
const headers = [
  { key: "product.name", title: "Name", fixed: true },
  { key: "price", title: "Price", width: 100 },
  { key: "amount_to_buy", title: "To buy", width: 100 },
  { key: "match", width: 1, sortable: false },
  { key: "amount_bought", title: "Bought", width: 100 },
  { key: "total", title: "Total", width: 150 },
  { key: "actions", sortable: false }
]
const editing = ref(false)

function toggleEditing() {
  editing.value = !editing.value

}

const list_total = computed(() => {
  return Intl.NumberFormat('en-US', { minimumFractionDigits: 2 }).format(products.value.reduce((prev, curr) => {
    return prev + curr.price * curr.amount_bought
  }, 0))
})

function itemFilter(value, query, item) {
  const normalizedName = item.raw.product.name.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const normalizedQuery = query.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  return normalizedName.includes(normalizedQuery)
}

function deleteItem(item) {
  axios.delete(`/shopping-lists/${list.value.id}/product/${item.value.product.id}`).then(() => {
    products.value.splice(products.value.indexOf(item.value), 1)
  }).catch(() => {
    // TODO: add alert
    console.error("Não foi possível remover");
  })
}

function itemSelected(item) {
  products.value.push(item)
}

function matchAmounts(item) {
  item.value.amount_bought = item.value.amount_to_buy
  const el = document.getElementById(`bought_${item.value.product.id}`)
  el.dispatchEvent(new Event('change'))
}

watch(list, () => {
  axios
    .patch(`/shopping-lists/${list.value.id}`, list.value)
    .catch(() => {
      // TODO: add alert
      // TODO: update to previous value
    })
}, { deep: true })

function handleChange(item_id, attribute, value) {
  axios
    .patch(`/shopping-lists/${list.value.id}/product/${item_id}`, {
      [attribute]: value
    })
    .catch(() => {
      // TODO: add alert
      // TODO: update to previous value
    })
}

onMounted(() => {
  axios.get(`shopping-lists/${route.params.id}`)
    .then((resp) => {
      let { products: product_list, ...rest } = resp.data
      list.value = rest
      products.value = product_list
    })
})

</script>