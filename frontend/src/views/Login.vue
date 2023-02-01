<template>
  <v-container>
    <v-row>
      <v-col>
        <Form as="v-form">
          <v-card class="mx-auto" max-width="600">
            <v-card-title> Login </v-card-title>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col>
                    <v-snackbar v-model="diag">
                      <v-alert :text="text" type="error" />
                    </v-snackbar>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <Field name="username" v-model="username" rules="required|min:4|max:16" v-slot="{ field, errors }">
                      <v-text-field v-bind="field" id="username" label="Username" @keyup.enter="submit" :error-messages="errors" />
                    </Field>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <Field name="password" v-model="password" rules="required" v-slot="{ field, errors }">
                    <v-text-field v-bind="field" label="Password" type="password" @keyup.enter="submit" :error-messages="errors"
                      persistent-clear />
                    </Field>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" @click.prevent="submit">Login</v-btn>
            </v-card-actions>
          </v-card>
        </Form>
      </v-col>
    </v-row>
  </v-container>
</template>
<script setup>
import router from "@/router";
import { inject, ref, onMounted, nextTick } from "vue";
import { Form, Field } from "vee-validate"
import qs from "qs";

const axios = inject("axios");
const username = ref("");
const password = ref("");
const diag = ref(false);
const text = ref("");

const submit = () => {
  axios
    .post(
      "auth/login",
      qs.stringify({
        username: username.value,
        password: password.value,
      })
    )
    .then((resp) => {
      localStorage.setItem("access_token", resp.data.access_token);
      localStorage.setItem("refresh_token", resp.data.refresh_token);
      router.push("shopping-lists");
    })
    .catch((err) => {
      diag.value = true;
      text.value = err.response.data.detail;
    });
};

onMounted(() => {
  nextTick(() => {
    document.getElementById("username").focus()
  })
})
</script>