<template>
  <v-text-field v-model="formattedValue" ref="inputRef"></v-text-field>
</template>
<script>
import { useCurrencyInput } from "vue-currency-input";

export default {
  name: "VCurrencyInput",
  props: {
    modelValue: Number,
    options: Object,
  },
  setup(props) {
    const options = {
      "locale": "en-US",
      "currency": "USD",
      "currencyDisplay": "hidden",
      "valueRange": {
        "min": 0
      },
      "precision": 2,
      "autoDecimalDigits": true,
      "useGrouping": true,
      "accountingSign": false,
      ...props.options
    }
    const { inputRef, formattedValue } = useCurrencyInput(options);

    return { inputRef, formattedValue };
  },
};
</script>