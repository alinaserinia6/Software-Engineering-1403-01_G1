<template>
  <div class="q-pa-md row items-start q-gutter-md">
    <q-card class="my-card" flat bordered>
      <q-card-section horizontal>
        <q-card-section class="q-pt-xs">
          <div class="text-h5 q-mt-sm q-mb-xs">Amin</div>
          <div class="text-caption text-grey">
            id
          </div>
        </q-card-section>

        <q-card-section class="col-5 flex flex-center">
          <q-img class="rounded-borders"
            src="https://cdn.quasar.dev/img/parallax2.jpg"
          />
        </q-card-section>
      </q-card-section>

      <q-separator />

      <q-card-actions>
        <q-btn flat>
          {{ currentTime }}
        </q-btn>
        <q-btn flat color="primary" @click="sendRequest">
          Request
        </q-btn>
      </q-card-actions>
    </q-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useChatStore } from '../stores/chat'

const chatStore = useChatStore()
const currentTime = ref('')

function updateTime() {
  const date = new Date()
  const hours = date.getHours()
  const minutes = date.getMinutes()
  const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}PM`
  if (hours < 12) {
    formattedTime.replace('PM', 'AM')
  }
  currentTime.value = formattedTime
}

onMounted(() => {
  updateTime()
  setInterval(updateTime, 60000) // update every minute
})

function sendRequest() {
  // Assuming you have the partner's ID
  const partnerId = 'partner-id'
  chatStore.sendLanguagePartnerRequest(partnerId)
}
</script>