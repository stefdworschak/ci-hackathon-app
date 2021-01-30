echo "Trying to export ERD"
python manage.py graph_models -a > erd.dot
dot -Tpng erd.dot -o erd.png
rm erd.dot
echo "Finished"