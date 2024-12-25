# <template>
#     <div>
#       <h2>Login</h2>
#       <form @submit.prevent="login">
#         <input v-model="email" placeholder="Email" required />
#         <input v-model="password" type="password" placeholder="Password" required />
#         <input v-model="role" type="role" placeholder="role" required />
#         <button type="submit">Login</button>
#       </form>
#     </div>
#   </template>
  
#   <script>
#   export default {
#     data() {
#       return {
#         email: '',
#         password: '',
#       };
#     },
#     methods: {
#       async login() {
#         const response = await fetch('http://localhost:8000/login/', {
#           method: 'POST',
#           headers: { 'Content-Type': 'application/json' },
#           body: JSON.stringify({ email: this.email, password: this.password, role: this.role }),
#         });
  
#         if (response.ok) {
#           const data = await response.json();
#           alert(`Welcome, ${data.message}`);
#           this.$emit('login', data.role);
#         } else {
#           alert('Invalid credentials');
#         }
#       },
#     },
#   };
#   </script>
  