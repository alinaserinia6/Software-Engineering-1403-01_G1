<template>
  <q-layout view="hhh lpR fFf">
    <q-header reveal bordered class="bg-primary text-white flex justify-center">
      <q-toolbar>
        <q-toolbar-title class="text-center"> Find your partner </q-toolbar-title>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <div class="q-pa-md row items-start q-gutter-md">
        <!-- Fake Partner Cards -->
        <q-card v-for="user in fakeUsers" :key="user.id" class="my-card" flat bordered>
          <q-card-section horizontal>
            <q-card-section class="q-pt-xs">
              <div class="text-h5 q-mt-sm q-mb-xs">{{ user.name }}</div>
              <div class="text-caption text-grey">
                ID: {{ user.id }}
              </div>
              <div class="text-caption text-green">
                Online
              </div>
              <div class="text-caption text-grey">
                {{ currentTime }}
              </div>
            </q-card-section>

            <q-card-section class="col-5 flex flex-center">
              <q-img class="rounded-borders" :src="user.avatar" />
            </q-card-section>
          </q-card-section>

          <q-separator />

          <q-card-actions>
            <q-btn v-if="!user.requestSent" flat color="primary" @click="sendRequest(user.id)">
              Request
            </q-btn>
            <q-btn v-else-if="user.requestAccepted" flat color="positive" @click="goToChatRoom(user.id)">
              Chat
            </q-btn>
            <q-btn v-else flat color="warning">
              Pending
            </q-btn>
          </q-card-actions>
        </q-card>
      </div>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// Fake users data
const fakeUsers = ref([
  {
    id: 1,
    name: 'کاظم',
    avatar: 'https://cdn.quasar.dev/img/avatar1.jpg',
    requestSent: false,
    requestAccepted: false,
  },
  {
    id: 2,
    name: 'قاسم',
    avatar: 'https://cdn.quasar.dev/img/avatar2.jpg',
    requestSent: false,
    requestAccepted: false,
  },
  {
    id: 3,
    name: 'جاسم',
    avatar: 'https://cdn.quasar.dev/img/avatar3.jpg',
    requestSent: false,
    requestAccepted: false,
  },
])

// Current time
const currentTime = ref(new Date().toLocaleTimeString())

// Update the current time every second
let interval
onMounted(() => {
  interval = setInterval(() => {
    currentTime.value = new Date().toLocaleTimeString()
  }, 1000)
})

// Clear the interval when the component is unmounted
onUnmounted(() => {
  clearInterval(interval)
})

// Send a chat request to a user
function sendRequest(partnerId) {
  const user = fakeUsers.value.find(user => user.id === partnerId)
  if (user) {
    user.requestSent = true
  }
  alert('Request sent!')
}

// Navigate to the chat room
function goToChatRoom(partnerId) {
  router.push({ name: 'chatroom', params: { partnerId } })
}
</script>

<style scoped>
.my-card {
  width: 100%;
  max-width: 300px;
}

.text-green {
  color: green;
}
</style>