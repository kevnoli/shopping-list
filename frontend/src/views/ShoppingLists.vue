<template>
  <v-card>
    <v-card-title>
      <div class="d-flex">
        Minhas listas
        <v-spacer />
        <v-dialog v-model="dialog">
          <template #activator="{ props }">
            <v-btn v-bind="props" icon="mdi-plus" variant="flat" />
          </template>
          <Form @submit="saveList">
            <v-card>
              <v-card-title>
                Add list
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col>
                      <Field name="name" v-model="list.name" rules="required" v-slot="{ field, errors }">
                        <v-text-field v-bind="field" autofocus label="Name" variant="underlined"
                          :error-messages="errors" />
                      </Field>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer />
                <v-btn color="primary" type="submit">Salvar</v-btn>
              </v-card-actions>
            </v-card>
          </Form>
        </v-dialog>
      </div>
    </v-card-title>
    <v-card-text>
      <v-data-table :headers="headers" :items="lists" @click:row.prevent="openDetails">
        <template #item.created_at="{ item }">
          {{ dayjs(item.raw.created_at).format("YYYY-MM-DD") }}
        </template>
        <template #item.updated_at="{ item }">
          {{ dayjs(item.raw.updated_at).format("YYYY-MM-DD") }}
        </template>
      </v-data-table>
    </v-card-text>
  </v-card>
</template>
<script setup>
import { inject, onMounted, ref } from "vue";
import dayjs from "dayjs";
import { useRouter } from "vue-router";
import { Form, Field } from "vee-validate";

const router = useRouter();
const axios = inject("axios");

const dialog = ref(false)
const lists = ref([]);
const list = ref({});
const headers = [
  { key: "name", title: "Name" },
  { key: "created_at", title: "Created at" },
  { key: "updated_at", title: "Updated at" },
]

function openDetails(ev, data) {
  return router.push(`/shopping-list/${data.item.raw.id}`);
}

function saveList() {
  axios
    .post("/shopping-lists", list.value)
    .then((resp) => {
      return router.push(`/shopping-list/${resp.data.id}`);
    })
}

onMounted(() => {
  axios.get("shopping-lists").then((resp) => {
    lists.value = resp.data
  });
});
</script> 