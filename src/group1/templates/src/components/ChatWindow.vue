<template>
  <div class="chat-window q-pa-md flex flex-center">
    <!-- Fake Chat Messages -->
    <div class="chat-messages">
      <q-chat-message v-for="message in messages"
        :key="message.id"
        :text="[message.content]"
        :sent="message.sent"
        :stamp="formatTimestamp(message.timestamp)"
        :class="message.sent ? 'sent-message' : 'received-message'"
      >
        <template v-slot:default>
          <q-menu context-menu>
            <q-list dense>
              <q-item clickable @click="editMessage(message.id)">
                <q-item-section>Edit</q-item-section>
              </q-item>
              <q-item clickable @click="deleteMessage(message.id)">
                <q-item-section>Delete</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </template>
      </q-chat-message>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// Fake chat messages
const messages = ref([
  {
    id: 1,
    content: 'Hello',
    sent: true,
    timestamp: new Date().toISOString(),
  },
  {
    id: 2,
    content: 'Hi!',
    sent: false,
    timestamp: new Date().toISOString(),
  },
  {
    id: 3,
    content: 'sdsd',
    sent: true,
    timestamp: new Date().toISOString(),
  },
  {
    id: 4,
    content: 'aasas',
    sent: false,
    timestamp: new Date().toISOString(),
  },
  {
    id: 5,
    content: 'qwqewe',
    sent: true,
    timestamp: new Date().toISOString(),
  },
])

// Format timestamp to hide seconds counter
function formatTimestamp(timestamp) {
  const date = new Date(timestamp)
  const hours = date.getHours()
  const minutes = date.getMinutes()
  const ampm = hours >= 12 ? 'PM' : 'AM'
  return `${hours % 12 || 12}:${minutes.toString().padStart(2, '0')} ${ampm}`
}

// Delete a message
function deleteMessage(messageId) {
  messages.value = messages.value.filter(message => message.id !== messageId)
}

// Edit a message
function editMessage(messageId) {
  const updatedContent = prompt('Edit your message:', messages.value.find(message => message.id === messageId).content)
  if (updatedContent) {
    const message = messages.value.find(message => message.id === messageId)
    if (message) {
      message.content = updatedContent
    }
  }
}
</script>

<style scoped>
.chat-window {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.chat-messages {
  width: 80%;
  max-width: 600px;
  background-color: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Sent message styling (Blue) */
.sent-message .q-chat-message-text {
  background-color: #007bff; /* Blue background for sent messages */
  color: white; /* White text for sent messages */
  border-radius: 15px 15px 0 15px; /* Rounded corners */
  padding: 10px 15px;
}

/* Received message styling (Green) */
.received-message .q-chat-message-text {
  background-color: #28a745; /* Green background for received messages */
  color: white; /* White text for received messages */
  border-radius: 15px 15px 15px 0; /* Rounded corners */
  padding: 10px 15px;
}

/* Timestamp styling */
.q-chat-message-stamp {
  font-size: 0.8rem; /* Decrease timestamp font size */
  color: #666; /* Change timestamp color */
}
</style>