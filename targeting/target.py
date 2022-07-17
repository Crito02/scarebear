import time

class targeter():
    def __init__(self):
        self.target_id = 0
        self.time_aquired = time.time()

    def body_no_face_then_latest(self, box_ids):
        """
        targets a body id that has never had a face

        box_ids: list of boxes
                x, y, z, w, h, id, faces
        return target id
        """
        
        latest = [0,0,0,0,0,0]
        face = False

        # Find newest and detect a face
        if box_ids != []:
            for body in box_ids:
                print("body")
                if body[4] > latest[4]:
                    latest = body
                if body[5]:
                    face = True
                    break
        
        # Update target list 
        result = 0
        if not face:
            if latest != [0,0,0,0,0,0]:
                if self.target_id != latest[4]:
                    self.time_aquired = time.time()
                    self.target_id = latest[4]
                print(self.target_id)
                    
            print(self.time_aquired)
            if time.time() > self.time_aquired + 2:
                result = self.target_id
        return result
        
    def latest_face(self, box_ids):
        """
        targets a body id that has never had a face

        box_ids: list of boxes
                x, y, z, w, h, id, faces
        return target id
        """
        
        latest = [0,0,0,0,0,0]
        face = False

        # Find newest and detect a face
        if box_ids != []:
            for body in box_ids:
                print("body")
                if body[4] > latest[4]:
                    latest = body
                if body[5]:
                    face = True
                    break
        
        # Update target list 
        result = 0
        if face:
            if latest != [0,0,0,0,0,0]:
                if self.target_id != latest[4]:
                    self.time_aquired = time.time()
                    self.target_id = latest[4]
                print(self.target_id)
                    
            print(self.time_aquired)
            if time.time() > self.time_aquired + 2:
                result = self.target_id
        return result


