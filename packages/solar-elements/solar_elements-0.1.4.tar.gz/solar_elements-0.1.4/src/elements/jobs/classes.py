from elements.posts import Post, Posts

#              /                         
#             /                          
#       #####/#                          
#       \   / #                          
#       #\ /  #                          
#       ##V####                          
#                                        
#        Jobs

# Jobs are posts with added functionality
# for keeping track of a completion status

class Job(Post):
    directory = "jobs"

    @property
    def is_done(self):
        return self.status == "complete"

    @property
    def status(self):
        return self.tags.getfirst('status') or "incomplete"

    @status.setter
    def status(self, value):
        self.tags.replace('status', [value])

    def complete(self):
        self.status = 'complete'

class Jobs(Posts):
    directory = "jobs"
    default_class = Job

    class_map = {
        Job.kind: Job
    }

    buckets = {
        **Posts.buckets,
        'status': lambda e: e.status
    }
