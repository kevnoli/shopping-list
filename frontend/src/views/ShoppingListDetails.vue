<template>
  <v-card>
    <v-card-text>
      <div class="d-flex align-center">
        <v-text-field id="list-name" :model-value="list.name" @change="(event) => list.name = event.target.value"
          variant="plain" hide-details />
        <v-spacer />
        <h2>$ {{ list_total }}</h2>
      </div>
      <div class="d-flex my-4">
        <v-spacer></v-spacer>
        <v-btn @click="deleteList" :icon="deleteIcon" variant="flat" />
        <v-btn @click="productDialog = true" icon="mdi-cart-plus" variant="flat" />
      </div>
      <product-search v-model="productDialog" @selected="itemSelected" />
      <v-data-table v-model:sort-by="sortBy" :headers="headers" :items="products" item-value="product.id"
        :search="search" :custom-filter="itemFilter" multi-sort dense>
        <template #top>
          <v-text-field id="search" v-model="search" @click="handleClick" label="Search" density="compact"
            variant="solo" single-line clearable />
        </template>
        <template #item.price="{ item }">
          <v-currency-input v-model="item.raw.price" @change="handleChange(item.value, 'price', item.raw.price)"
            @click="handleClick" prefix="$" class="pb-3" density="compact" variant="plain" single-line hide-details
            :readonly="item.raw.completed" />
        </template>
        <template #item.amount_to_buy="{ item }">
          <v-text-field v-model="item.raw.amount_to_buy"
            @change="handleChange(item.value, 'amount_to_buy', item.raw.amount_to_buy)" @click="handleClick"
            class="pb-3" density="compact" variant="plain" single-line hide-details :readonly="item.raw.completed" />
        </template>
        <template #item.match="{ item }">
          <v-btn flat size="small" icon="mdi-link" @click="matchAmounts(item)" />
        </template>
        <template #item.amount_bought="{ item }">
          <v-text-field :id="`bought_${item.value}`" v-model="item.raw.amount_bought"
            @change="handleChange(item.value, 'amount_bought', item.raw.amount_bought)" @click="handleClick"
            class="pb-3" density="compact" variant="plain" single-line hide-details :readonly="item.raw.completed" />
        </template>
        <template #item.total="{ item }">
          <v-text-field
            :model-value="Intl.NumberFormat('en-US', { minimumFractionDigits: 2 }).format(Math.round((item.raw.price * item.raw.amount_bought + Number.EPSILON) * 100) / 100)"
            prefix="$" class="pb-3" density="compact" variant="plain" single-line hide-details readonly />
        </template>
        <template #item.actions="{ item }">
          <v-btn flat size="small" :icon="item.raw.completed ? 'mdi-pencil' : 'mdi-check'"
            @click="updateCompleted(item)" />
          <v-btn flat size="small" icon="mdi-delete" @click="deleteItem(item)" />
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { inject, onMounted, ref, watch, computed, nextTick } from "vue";
import { useRoute, useRouter } from 'vue-router';

import ProductSearch from "@/components/ProductSearch.vue";

const route = useRoute()
const router = useRouter()
const axios = inject("axios")

const productDialog = ref(false)
const list = ref({})
const products = ref([])
const search = ref("")
const headers = [
  { key: "product.name", title: "Name", fixed: true },
  { key: "price", title: "Price", width: 150 },
  { key: "amount_to_buy", title: "To buy", width: 1 },
  { key: "match", width: 1, sortable: false },
  { key: "amount_bought", title: "Bought", width: 100 },
  { key: "total", title: "Total", width: 150, sortable: false },
  { key: "actions", sortable: false },
]
const sortBy = ref([
  { key: "completed", order: "asc" },
])

const list_total = computed(() => {
  return Intl.NumberFormat('en-US', { minimumFractionDigits: 2 }).format(Math.round((products.value.reduce((prev, curr) => {
    return prev + curr.price * curr.amount_bought
  }, 0) + Number.EPSILON) * 100) / 100)
})

function itemFilter(value, query, item) {
  const normalizedName = item.raw.product.name.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const normalizedQuery = query.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  return normalizedName.includes(normalizedQuery)
}

function deleteItem(item) {
  axios.delete(`/shopping-lists/${list.value.id}/product/${item.value}`)
    .then(() => {
      products.value.splice(products.value.indexOf(item.raw), 1)
    })
    .catch(() => {
      // TODO: add alert
      console.error("Não foi possível remover");
    })
}

function itemSelected(item) {
  products.value.push(item)
}

function matchAmounts(item) {
  item.raw.amount_bought = item.raw.amount_to_buy
  const el = document.getElementById(`bought_${item.value}`)
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

watch(productDialog, (value) => {
  if (!value) {
    nextTick(() => {
      document.getElementById("search").focus()
    })
  }
})

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

function handleClick(ev) {
  ev.target.select()
}

const deleteIcon = ref("mdi-delete")
function deleteList() {
  if (deleteIcon.value == "mdi-delete") {
    deleteIcon.value = "mdi-delete-alert"
    setTimeout(() => deleteIcon.value = "mdi-delete", 3000)
  } else {
    axios
      .delete(`/shopping-lists/${list.value.id}`)
      .then(() => {
        router.push("/shopping-lists")
      })
  }
}

function updateCompleted(item) {
  item.raw.completed = !item.raw.completed
  axios
    .patch(`/shopping-lists/${list.value.id}/product/${item.value}`, {
      "completed": Boolean(item.raw.completed)
    })
    .catch(() => {
      // TODO: add alert
      item.raw.completed = !item.raw.completed
    })
}

onMounted(() => {
  axios.get(`shopping-lists/${route.params.id}`)
    .then((resp) => {
      let { products: product_list, ...rest } = resp.data
      list.value = rest
      products.value = product_list
    })
    .catch((err) => {
      if (err.response.status == 404) {
        router.back()
      }
    })
  nextTick(() => {
    document.getElementById("search").focus()
  })
})

</script>
<style>
#list-name {
  font-size: x-large;
  font-weight: bold;
}
</style>