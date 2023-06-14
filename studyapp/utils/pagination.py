from django.utils.safestring import mark_safe
import copy
class Pagination(object):
    def __init__(self,req, query_set, page_size=9,page_param='page',plus=4):
        

        query_dict = copy.deepcopy(req.GET)
        query_dict._mutable = True
        self.query_dict = query_dict     
        self.page_param = page_param
        page = req.GET.get(page_param,"1")
        if page.isdecimal():
              page = int(page)
        else:
              page=1
        self.plus = plus
        self.page = page 
        self.page_size=page_size
   
        #the data is filtered by page
        self.start=(page-1)*page_size
        self.end = page*page_size
        self.page_queryset = query_set[self.start:self.end]  
        # the count of all pages
        total_count = query_set.count()
        total_page_count, div =divmod(total_count,page_size)   
        if div:
            total_page_count+=1
        self.total_page_count = total_page_count

        #the start page index and the end page index
        if self.total_page_count <= 2*self.plus+1:
          self.start_page_index=1
          self.end_page_index = self.total_page_count
        else:
          if self.page<=self.plus:
              self.start_page_index=1
              self.end_page_index=2*self.plus+1
          else:
              if self.page+self.plus>self.total_page_count:
                  self.start_page_index = self.total_page_count-2*self.plus
                  self.end_page_index = self.total_page_count
              else:
                  self.start_page_index = self.page-self.plus
                  self.end_page_index = self.page+self.plus
        
    def html(self):    
      page_str_list = []

      self.query_dict.setlist(self.page_param,[1])

      firstPage = '<li  class="page-item"><a  class="page-link"" href="?{}">First</a></li>'.format(self.query_dict.urlencode())
      page_str_list.append(firstPage)
      if self.page>1:
          preNum = self.page-1
      else:
          preNum=1
      self.query_dict.setlist(self.page_param,[preNum])
      prePage = '<li  class="page-item"><a  class="page-link"" href="?{}"><<</a></li>'.format(self.query_dict.urlencode())
      page_str_list.append(prePage)

      for i in range(self.start_page_index,self.end_page_index+1):
          self.query_dict.setlist(self.page_param,[i])
          
          if i==self.page:
            ele = '<li  class="page-item active"><a  class="page-link"" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i)
          else:
            ele = '<li  class="page-item "><a  class="page-link"" href="?{}">{}</a></li>'.format(self.query_dict.urlencode(),i)

          page_str_list.append(ele)


      if self.page<self.total_page_count:
          nextNum = self.page+1
      else:
          nextNum=self.total_page_count
      
      self.query_dict.setlist(self.page_param,[nextNum])
      
      nextPage = '<li  class="page-item"><a  class="page-link"" href="?{}">>></a></li>'.format(self.query_dict.urlencode())
      page_str_list.append(nextPage)

      self.query_dict.setlist(self.page_param,[self.total_page_count])

      lastPage = '<li  class="page-item"><a  class="page-link"" href="?{}">Last</a></li>'.format(self.query_dict.urlencode())
      page_str_list.append(lastPage)

      jump_string = """
      <li>
        <form action="" method="get">
          <div class="input-group" style="width: 240px">
            <input
              type="text"
              name="page"
              class="form-control"
              placeholder="Page Number"
            />
            <button class="btn btn-success" type="submit" value="1">Jump</button>
          </div>
        </form>
      </li>
      """
      page_str_list.append(jump_string)
      page_string = mark_safe("".join(page_str_list))
      return page_string

      
