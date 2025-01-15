const routes = [
  {
    path: '',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', name : 'login' , component: () => import('src/pages/LoginPage.vue') },
      { path: 'SignUp', name : 'signup' , component: () => import('src/pages/SingupPage.vue') },
      { path: 'PartnerList', name : 'partnerlist' , component: () => import('src/pages/PartnerList.vue') },
      { path: 'ChatRoom/:partnerId', name : 'chatroom' , component: () => import('src/pages/ChatRoom.vue') }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
