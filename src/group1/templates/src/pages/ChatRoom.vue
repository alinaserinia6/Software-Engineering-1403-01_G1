<template>
  <div class="chat-room-container">
    <div class="drawer-container" :class="{ 'drawer-open': isDrawerOpen }">
      <chat-info-and-drawer :is-drawer-open="isDrawerOpen" @toggle-drawer="toggleDrawer" />
    </div>

    <div class="chat-content-container">
      <chat-window :messages="messages" />
      <message-input @sendMessage="handleSendMessage" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted} from 'vue'
import { useChatStore } from 'src/stores/chat'
import { useRoute } from 'vue-router'
import ChatInfoAndDrawer from 'src/components/ChatInfoAndDrawer.vue'
import ChatWindow from 'src/components/ChatWindow.vue'
import MessageInput from 'src/components/MessageInput.vue'

const chatStore = useChatStore()
const route = useRoute()
const isDrawerOpen = ref(false)
const messages = ref([])
const partnerId = route.params.partnerId

// Fetch messages when the page loads
onMounted(async () => {
  await chatStore.getAllChats()
  const chat = chatStore.chats.find(chat => chat.partnerId === partnerId)
  if (chat) {
    messages.value = chat.messages
  }
})

// Send a message
async function handleSendMessage(message) {
  await chatStore.sendMessageInPrivateChat(partnerId, message)
  messages.value.push({ content: message, sent: true })
}

function toggleDrawer() {
  isDrawerOpen.value = !isDrawerOpen.value
}

</script>

<style scoped>
.chat-room-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.drawer-container {
  width: 0;
  transition: width 0.3s ease;
  overflow: hidden;
}

.drawer-container.drawer-open {
  width: 250px;
}

.chat-content-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  margin-left: 0;
  transition: margin-left 0.3s ease;
}
</style>