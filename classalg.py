import json

def classalg():
    # Load student and class data
    with open('studentdat.json', 'r') as sf:
        student_data = json.load(sf)["students"]
    with open('classdat.json', 'r') as cf:
        class_data = json.load(cf)["classes"]

    # Prepare class block mapping
    class_block_map = {
        class_name: class_info["Blocks"]
        for class_name, class_info in class_data.items()
    }

    def score_student_class(student_topics, class_topics):
        """Calculate compatibility score between student and class (lower is better)."""
        score = 0
        for topic, student_score in student_topics.items():
            class_score = int(class_topics.get(topic, 0))
            score += abs(int(student_score) - class_score)
        return score

    def assign_classes_to_student(sorted_class_scores, class_block_map):
        """Assign up to 5 non-conflicting classes to a student."""
        assigned = []
        used_blocks = set()
        for class_name, _ in sorted_class_scores:
            for block in class_block_map.get(class_name, []):
                if block not in used_blocks:
                    assigned.append((class_name, block))
                    used_blocks.add(block)
                    break
            if len(assigned) >= 5:
                break
        return assigned

    # Process each student
    for student_name, student_info in student_data.items():
        student_topics = student_info["Topics"]

        # Compute and sort class scores
        class_scores = []
        for class_name, class_info in class_data.items():
            class_topics = class_info["Topics"]
            score = score_student_class(student_topics, class_topics)
            class_scores.append((class_name, score))

        sorted_scores = sorted(class_scores, key=lambda x: x[1])

        # Assign classes avoiding block conflicts
        final_schedule = assign_classes_to_student(sorted_scores, class_block_map)

        # Print result
        if final_schedule:
            schedule_str = ', '.join([f"{cls} (Block {blk})" for cls, blk in final_schedule])
            print(f"{student_name}: {schedule_str}")
        else:
            print(f"{student_name}: No classes assigned.")

# Call the function
classalg()