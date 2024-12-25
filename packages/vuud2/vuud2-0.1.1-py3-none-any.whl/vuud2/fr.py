# npm create vue@latest

# <script>
# import LoginForm from './components/LoginForm.vue';
# import BooksList from './components/BookList.vue';
# import CreateBook from './components/CreateBook.vue';

# export default {
#   components: { LoginForm, BooksList, CreateBook },
#   data() {
#     return {
#       books: [],
#       isManager: false,
#     };
#   },
#   methods: {
#     handleLogin(role) {
#       this.isManager = role === 'manager';
#       this.fetchBooks();
#     },
#     async fetchBooks() {
#       const response = await fetch('http://localhost:8000/books/');
#       this.books = await response.json();
#     },
#   },
#   mounted() {
#     this.fetchBooks();
#   },
# };
# </script>

# <template>
#   <div>
#     <h1>Name</h1>
#     <LoginForm @login="handleLogin" />
#     <CreateBook v-if="isManager" @bookCreated="fetchBooks" />
#     <BooksList :books="books" />
#   </div>
# </template>

