# <template>
#     <div>
#       <h2>Name</h2>
#       <ul>
#         <li v-for="book in books" :key="book.id">
#           {{ book.title }} by {{ book.author || 'Unknown Author' }}
#         </li>
#       </ul>
#     </div>
#   </template>
  
#   <script>
#   export default {
#     props: ['books'],
#   };
#   </script>
  