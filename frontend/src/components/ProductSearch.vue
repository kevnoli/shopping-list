<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title>
        Search items
      </v-card-title>
      <v-card-text>
        <v-text-field v-model="query" label="Name" autofocus clearable append-icon="mdi-magnify"
          @click:append="searchItem" @keyup.enter="searchItem" />
        <v-data-table v-if="items" :headers="headers" :items="items">
          <template #item.price="{ item }">
            <v-currency-input v-model="item.raw.price" prefix="$" class="pb-3" density="compact" variant="plain"
              single-line hide-details />
          </template>
          <template #item.amount_to_buy="{ item }">
            <v-amount-input :options="{ 'precision': item.raw.unit.precision }" :suffix="item.raw.unit.name"
              v-model="item.raw.amount_to_buy" class="pb-3" density="compact" variant="plain" single-line
              hide-details />
          </template>
          <template #item.actions="{ item }">
            <v-btn flat size="small" icon="mdi-check" @click="selectItem(item.raw)" />
          </template>
          <template #no-data>
            <tr v-if="searched">
              <td :colspan="headers.length" style="text-align: center; vertical-align: middle;">
                Item not found.
                <v-dialog v-model="addDialog">
                  <template #activator="{ props }">
                    <v-btn v-bind="props" variant="text" color="primary" @click="item.name = query">Add?</v-btn>
                  </template>
                  <v-card>
                    <Form @submit="addItem">
                      <v-card-title>
                        Add item
                      </v-card-title>
                      <v-card-text>
                        <Field name="name" v-model="item.name" v-slot="{ field, errors }" rules="required">
                          <v-text-field v-bind="field" :error-messages="errors" />
                        </Field>
                        <Field name="unit" v-model="item.unit_id" v-slot="{ field, errors }" rules="required">
                          <v-select :items="units" item-title="name" item-value="id" v-bind="field" :error-messages="errors" />
                        </Field>
                      </v-card-text>
                      <v-card-actions>
                        <v-spacer />
                        <v-btn color="primary" type="submit">Add</v-btn>
                      </v-card-actions>
                    </Form>
                  </v-card>
                </v-dialog>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>
<script setup>
import { inject, ref, computed, onMounted } from "vue"
import { useRoute } from "vue-router";
import { Form, Field } from 'vee-validate'

const axios = inject("axios")
const route = useRoute()
const emit = defineEmits(['selected', 'update:modelValue'])
const props = defineProps(['modelValue'])

const searched = ref(false)
const dialog = computed({
  get() {
    return props.modelValue
  },
  set(value) {
    emit('update:modelValue', value)
  }
})
const addDialog = ref(false)

const query = ref("")
const item = ref({ name: "", unit_id: null })
const items = ref([])
const headers = [
  { key: "name", title: "Name" },
  { key: "price", title: "Price" },
  { key: "amount_to_buy", title: "To buy" },
  { key: "actions", title: "Actions" }
]
const units = ref([])

function addItem() {
  axios
    .post("products", item.value)
    .then((resp) => {
      let addedItem = resp.data
      addedItem.price = 0
      addedItem.amount_to_buy = 0
      addedItem.amount_bought = 0
      items.value.push(addedItem)
      addDialog.value = false
      selectItem(addedItem)
    })
}

function searchItem() {
  searched.value = true
  axios
    .get("products", {
      params: {
        query: query.value,
        exclude: route.params.id
      },
    })
    .then((resp) => {
      items.value = resp.data;
      items.value.forEach(el => {
        el.price = 0
        el.amount_to_buy = 0
        el.amount_bought = 0
      });
    })
}

function selectItem(item) {
  axios
    .post(`/shopping-lists/${route.params.id}/product`, {
      product_id: item.id,
      price: item.price,
      amount_to_buy: item.amount_to_buy
    })
    .then((resp) => {
      emit("selected", resp.data)
    })
}

onMounted(() => {
  axios
    .get("/units")
    .then((resp) => {
      units.value = resp.data
    })
})
</script>