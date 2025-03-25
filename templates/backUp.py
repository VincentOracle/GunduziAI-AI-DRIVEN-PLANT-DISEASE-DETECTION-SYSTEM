@app.route("/admin/reports/logged_users")
def get_logged_users_report():
    try:
        # Get date range from query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build base query
        query = db.session.query(
            func.date(Diagnosis_Results.Diagnosis_Date).label('date'),
            func.count(Diagnosis_Results.Result_ID).label('count')
        ).group_by(func.date(Diagnosis_Results.Diagnosis_Date))
        
        # Apply date filters if provided
        if start_date:
            query = query.filter(Diagnosis_Results.Diagnosis_Date >= start_date)
        if end_date:
            query = query.filter(Diagnosis_Results.Diagnosis_Date <= end_date)
        
        # Execute query and format results
        results = query.order_by(func.date(Diagnosis_Results.Diagnosis_Date)).all()
        
        # Format data for chart
        dates = [result.date.strftime('%Y-%m-%d') for result in results]
        counts = [result.count for result in results]
        
        return jsonify({
            "success": True,
            "labels": dates,
            "data": counts
        })
    except Exception as e:
        print(f"Error fetching logged users report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/reports/plant_diseases")
def get_plant_diseases_report():
    try:
        # Get date range from query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build base query
        query = db.session.query(
            Diagnosis_Results.Predicted_Disease,
            func.count(Diagnosis_Results.Result_ID).label('count')
        ).group_by(Diagnosis_Results.Predicted_Disease)
        
        # Apply date filters if provided
        if start_date and end_date:
            query = query.join(Plant_Images, Diagnosis_Results.Image_ID == Plant_Images.Image_ID)\
                        .filter(Plant_Images.Upload_Date >= start_date)\
                        .filter(Plant_Images.Upload_Date <= end_date)
        
        # Execute query and format results
        results = query.order_by(func.count(Diagnosis_Results.Result_ID).desc()).all()
        
        # Format data for chart
        diseases = [result.Predicted_Disease for result in results]
        counts = [result.count for result in results]
        
        return jsonify({
            "success": True,
            "labels": diseases,
            "data": counts
        })
    except Exception as e:
        print(f"Error fetching plant diseases report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/reports/user_feedback")
def get_user_feedback_report():
    try:
        # Get date range from query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build base query
        query = db.session.query(
            Feedback,
            Users.First_Name,
            Users.Last_Name,
            Users.Email
        ).join(Users, Feedback.User_ID == Users.User_ID)
        
        # Apply date filters if provided
        if start_date:
            query = query.filter(Feedback.Feedback_Date >= start_date)
        if end_date:
            query = query.filter(Feedback.Feedback_Date <= end_date)
        
        # Execute query and format results
        results = query.order_by(Feedback.Feedback_Date.desc()).all()
        
        # Format data for table
        feedback_data = [{
            "User_Name": f"{result.First_Name} {result.Last_Name}",
            "Email": result.Email,
            "Feedback_Text": result.Feedback.Feedback_Text,
            "Prediction_Accuracy": result.Feedback.Prediction_Accuracy,
            "System_Rating": result.Feedback.System_Rating,
            "Feedback_Date": result.Feedback.Feedback_Date.strftime('%Y-%m-%d')
        } for result in results]
        
        return jsonify({
            "success": True,
            "feedback": feedback_data
        })
    except Exception as e:
        print(f"Error fetching user feedback report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/reports/disease_trends")
def get_disease_trends_report():
    try:
        # Get date range from query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Build base query
        query = db.session.query(
            func.date(Diagnosis_Results.Diagnosis_Date).label('date'),
            Diagnosis_Results.Predicted_Disease,
            func.count(Diagnosis_Results.Result_ID).label('count')
        ).group_by(
            func.date(Diagnosis_Results.Diagnosis_Date),
            Diagnosis_Results.Predicted_Disease
        )
        
        # Apply date filters if provided
        if start_date:
            query = query.filter(Diagnosis_Results.Diagnosis_Date >= start_date)
        if end_date:
            query = query.filter(Diagnosis_Results.Diagnosis_Date <= end_date)
        
        # Execute query and format results
        results = query.order_by(func.date(Diagnosis_Results.Diagnosis_Date)).all()
        
        # Format data for chart
        dates = sorted(list(set([result.date.strftime('%Y-%m-%d') for result in results])))
        diseases = sorted(list(set([result.Predicted_Disease for result in results])))
        
        # Create dataset for each disease
        datasets = []
        for disease in diseases:
            disease_data = {result.date.strftime('%Y-%m-%d'): result.count 
                          for result in results if result.Predicted_Disease == disease}
            counts = [disease_data.get(date, 0) for date in dates]
            
            # Generate random color for each disease line
            color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.7)"
            
            datasets.append({
                "label": disease,
                "data": counts,
                "borderColor": color,
                "fill": False
            })
        
        return jsonify({
            "success": True,
            "labels": dates,
            "datasets": datasets
        })
    except Exception as e:
        print(f"Error fetching disease trends report: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
        
 

@app.route("/admin/reports/export_pdf")
def export_report_pdf():
    try:
        report_type = request.args.get('report_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Fetch data based on report type
        if report_type == "logged_users":
            data = get_logged_users_report().get_json()
            title = "Logged-In Users Report"
        elif report_type == "plant_diseases":
            data = get_plant_diseases_report().get_json()
            title = "Plant Diseases Report"
        elif report_type == "user_feedback":
            data = get_user_feedback_report().get_json()
            title = "User Feedback Report"
        elif report_type == "disease_trends":
            data = get_disease_trends_report().get_json()
            title = "Disease Trends Report"
        else:
            return jsonify({"success": False, "error": "Invalid report type"}), 400
        
        if not data.get("success"):
            return jsonify({"success": False, "error": data.get("error")}), 500
        
        # Generate PDF (in a real implementation, you would use a PDF library)
        # For now, we'll return the data and let the frontend handle PDF generation
        return jsonify({
            "success": True,
            "title": title,
            "data": data,
            "start_date": start_date,
            "end_date": end_date
        })
    except Exception as e:
        print(f"Error exporting report to PDF: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/admin/reports/export_excel")
def export_report_excel():
    try:
        report_type = request.args.get('report_type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # Fetch data based on report type
        if report_type == "logged_users":
            data = get_logged_users_report().get_json()
            title = "Logged-In Users Report"
            # Format data for Excel
            excel_data = [["Date", "User Count"]] + [
                [data["labels"][i], data["data"][i]] 
                for i in range(len(data["labels"]))
            ]
        elif report_type == "plant_diseases":
            data = get_plant_diseases_report().get_json()
            title = "Plant Diseases Report"
            excel_data = [["Disease", "Count"]] + [
                [data["labels"][i], data["data"][i]] 
                for i in range(len(data["labels"]))
            ]
        elif report_type == "user_feedback":
            data = get_user_feedback_report().get_json()
            title = "User Feedback Report"
            excel_data = [["User Name", "Email", "Feedback", "Accuracy", "Rating", "Date"]] + [
                [
                    item["User_Name"], 
                    item["Email"], 
                    item["Feedback_Text"],
                    item["Prediction_Accuracy"],
                    item["System_Rating"],
                    item["Feedback_Date"]
                ] 
                for item in data["feedback"]
            ]
        elif report_type == "disease_trends":
            data = get_disease_trends_report().get_json()
            title = "Disease Trends Report"
            # More complex formatting for disease trends
            excel_data = [["Date"] + data["datasets"][i]["label"] for i in range(len(data["datasets"]))]
            for i, date in enumerate(data["labels"]):
                row = [date]
                for dataset in data["datasets"]:
                    row.append(dataset["data"][i])
                excel_data.append(row)
        else:
            return jsonify({"success": False, "error": "Invalid report type"}), 400
        
        if not data.get("success"):
            return jsonify({"success": False, "error": data.get("error")}), 500
        
        # Generate Excel (in a real implementation, you would use an Excel library)
        # For now, we'll return the data and let the frontend handle Excel generation
        return jsonify({
            "success": True,
            "title": title,
            "data": excel_data,
            "start_date": start_date,
            "end_date": end_date
        })
    except Exception as e:
        print(f"Error exporting report to Excel: {e}")
        return jsonify({"success": False, "error": str(e)}), 500