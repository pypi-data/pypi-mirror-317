class EasilyAIPipeline:
    def __init__(self, app):
        self.app = app
        self.tasks = []

    def add_task(self, task_type, data):
        """
        Add a task to the pipeline.
        :param task_type: 'generate_text', 'generate_image', or 'text_to_speech'
        :param data: The input for the task (e.g., prompt or text).
        """
        self.tasks.append({"type": task_type, "data": data})

    def run(self):
        """
        Execute the tasks sequentially.
        """
        results = []
        for i, task in enumerate(self.tasks):
            task_type = task["type"]
            data = task["data"]

            print(f"Running Task {i + 1}: {task_type}")

            if task_type == "generate_text":
                result = self.app.request(data)
            elif task_type == "generate_image":
                result = self.app.request(f"Generate an image: {data}")
            elif task_type == "text_to_speech":
                result = self.app.client.text_to_speech(data)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            results.append({"task": task_type, "result": result})
        
        print("\nPipeline Completed!")
        return results
