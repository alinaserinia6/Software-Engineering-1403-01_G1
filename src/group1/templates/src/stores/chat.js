import { defineStore } from 'pinia'
import { api } from 'src/boot/axios'

export const useChatStore = defineStore('chat', {
  state: () => ({
    chats: [],
    users: [],
    messages: [],
    user: null,
    languagePartners: [],
    groups: []
  }),
  getters: {
  },
  actions: {
    // User Management
    async registerUser (data) {
      try {
        const response = await api.post('register/', data)
        this.user = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async loginUser(data) {
      try {
        const response = await api.post('login/', data)
        this.user = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async logoutUser () {
      try {
        await api.post('logout/')
        this.user = null
      } catch (error) {
        console.error(error)
      }
    },
    async editUserProfile(data) {
      try {
        const response = await api.post('profile/edit/', data)
        this.user = response.data
      } catch (error) {
        console.error(error)
      }
    },

    // Private Chat
    async createPrivateChat(data) {
      try {
        const response = await api.post('private-chat/create/', data)
        this.chats.push(response.data)
      } catch (error) {
        console.error(error)
      }
    },
    async sendMessageInPrivateChat(chatId, message) {
      try {
        const response = await api.post(`private-chat/${chatId}/send-message/`, { message })
        this.chats.find(chat => chat.id === chatId).messages.push(response.data)
      } catch (error) {
        console.error(error)
      }
    },
    async getPrivateChat(chatId) {
      try {
        const response = await api.get(`private-chat/${chatId}/`)
        return response.data
      } catch (error) {
        console.error(error)
      }
    },

    // Group Chat
    async createGroup(data) {
      try {
        const response = await api.post('group/create/', data)
        this.groups.push(response.data)
      } catch (error) {
        console.error(error)
      }
    },
    async sendMessageInGroup(groupId, message) {
      try {
        const response = await api.post(`group/${groupId}/send-message/`, { message })
        this.groups.find(group => group.id === groupId).messages.push(response.data)
      } catch (error) {
        console.error(error)
      }
    },
    async addMemberToGroup(groupId, memberId) {
      try {
        const response = await api.post(`group/${groupId}/add-member/`, { memberId })
        this.groups.find(group => group.id === groupId).members.push(response.data)
      } catch (error) {
        console.error(error)
      }
    },
    async removeMemberFromGroup(groupId, memberId) {
      try {
        const response = await api.post(`group/${groupId}/remove-member/`, { memberId })
        this.groups.find(group => group.id === groupId).members = response.data
      } catch (error) {
        console.error(error)
      }
    },

    // Language Partner Matching
    async searchLanguagePartners(data) {
      try {
        const response = await api.post('language-partners/search/', data)
        this.languagePartners = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async sendLanguagePartnerRequest(partnerId) {
      try {
        await api.post('language-partners/request/', { partnerId })
        this.languagePartners.find(partner => partner.id === partnerId).requestSent = true
      } catch (error) {
        console.error(error)
      }
    },
    async acceptLanguagePartnerRequest(partnerId) {
      try {
        await api.post('language-partners/accept/', { partnerId })
        this.languagePartners.find(partner => partner.id === partnerId).requestAccepted = true
      } catch (error) {
        console.error(error)
      }
    },

    // Reporting and Blocking
    async reportUser  (userId) {
      try {
        await api.post('report/', { userId })
        this.users.find(user => user.id === userId).reported = true
      } catch (error) {
        console.error(error)
      }
    },
    async blockUser  (userId) {
      try {
        await api.post('block/', { userId })
        this.users.find(user => user.id === userId).blocked = true
      } catch (error) {
        console.error(error)
      }
    },

    // User Retrieval
    async getAllUsers() {
      try {
        const response = await api.get('users/')
        this.users = response.data
      } catch (error) {
        console.error(error)
      }
    },
    async getSingleUser (userId) {
      try {
        const response = await api.get(`users/${userId}/`)
        return response.data
      } catch (error) {
        console.error(error)
      }
    },

    // Chat Retrieval
    async getAllChats() {
      try {
        const response = await api.get('chats/')
        this.chats = response.data
      } catch (error) {
        console.error(error)
      }
    },

    // Additional
    async getUserAvatar(userId) {
      try {
        const response = await api.get(`user/avatar/${userId}/`)
        return response.data
      } catch (error) {
        console.error(error)
      }
    },
    async getUserDetails(userId) {
      try {
        const response = await api.get(`user/details/${userId}/`)
        return response.data
      } catch (error) {
        console.error(error)
      }
    },

    // Message Management
    async deleteMessage(messageId) {
      try {
        await api.delete(`message/${messageId}/delete/`)
        this.messages = this.messages.filter(message => message.id !== messageId)
      } catch (error) {
        console.error(error)
      }
    },
    async editMessage(messageId, updatedContent) {
      try {
        const response = await api.post(`message/${messageId}/edit/`, { content: updatedContent })
        const message = this.messages.find(msg => msg.id === messageId)
        if (message) {
          message.content = response.data.content
        }
      } catch (error) {
        console.error(error)
      }
    }
  }
})