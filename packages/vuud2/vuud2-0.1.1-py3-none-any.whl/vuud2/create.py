# <template>
#     <div>
#       <h2>Name</h2>
#       <form @submit.prevent="createBook">
#         <input v-model="title" type="text" placeholder="Title" required />
#         <input v-model="author" type="text" placeholder="Author" />
#         <input v-model="publisher" type="text" placeholder="Publisher" required />
#         <input v-model="year" type="number" placeholder="Year" required />
#         <input v-model="pages" type="number" placeholder="Pages" required />
#         <input v-model="code" type="text" placeholder="Code" required />
#         <button type="submit">Create</button>
#       </form>
#     </div>
#   </template>
  
#   <script>
#   export default {
#     data() {
#       return {
#         title: '',
#         author: '',
#         publisher: '',
#         year: null,
#         pages: null,
#         code: '',
#       };
#     },
#     methods: {
#       async createBook() {
#         const response = await fetch('http://localhost:8000/books/', {
#           method: 'POST',
#           headers: { 'Content-Type': 'application/json' },
#           body: JSON.stringify({
#             title: this.title,
#             author: this.author,
#             publisher: this.publisher,
#             year: this.year,
#             pages: this.pages,
#             code: this.code,
#           }),
#         });
  
#         if (response.ok) {
#           alert('Book created successfully');
#           this.$emit('bookCreated');
#         } else {
#           alert('Failed to create book');
#         }
#       },
#     },
#   };
#   </script>
  