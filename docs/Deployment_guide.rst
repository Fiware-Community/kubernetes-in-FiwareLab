Introduction:
----------------------------------------------
This Document provide step by step guide user to do changes in code of FIWARE Lab GUI and provide a button in Overview tab of FIWARE LAB GUI to redirect to kubernetes support GUI.

**Step 1:** For deployment we have to do change in Horizon code so that we can get Project ID and Instance IP for all the instances on which user want to deploy kubernetes cluster.
To do so we have to do changes in views.py. 

The path for the file is :- /horizon/openstack_dashboard/dashboards/project/overview/views.py.

**Code Block:**

'''
from openstack_dashboard.dashboards.project.api_access.views \
    import _get_openrc_credentials as get_pid

from openstack_dashboard.dashboards.project.instances.views \
    import IndexView

from django.shortcuts import render, redirect
import urllib.parse

def kubernetes(request):
    print("button clicked")
    cred = get_pid(request)
    pid = cred['tenant_id']
    search_opts = {'marker': None, 'project_id': pid, 'limit': 21}
    sort_dir = "desc"
    indexView = IndexView()
    indexView.request = request
    instanceIP = []

    instances = indexView._get_instances(search_opts=search_opts, sort_dir=sort_dir)
    for i in range(len(instances)):
        instanceIP.append(instances[i].addresses['shared'][0]['addr'])

    a = ','.join(instanceIP)
    url = "http://180.179.214.158:5000/auth/"+str(pid)+"?ip="+str(a)
    return redirect(url)
'''

**Step 2:** For redirect we have to do changes in urls.py so that user should be redirected to kubernetes support GUI and button should be functional. 

The path for the file is :- /horizon/openstack_dashboard/dashboards/project/overview/urls.py.

**Code Block:**

'''
urlpatterns = [
    re_path(r'^$', views.ProjectOverview.as_view(), name='index'),
    re_path(r'^warning$', views.WarningView.as_view(), name='warning'),
    re_path(r'^kubernetes$', views.kubernetes, name='kubernetes_test'),
]
'''

**Step 3:** To show kubernetes button in horizon dashboard of FIWARE Lab GUI we have to do changes in usage.html file.

The path for the file is :- /horizon/openstack_dashboard/dashboards/project/overview//templates/overview/usage.html

**Code Block:**

'''
{% block main %}
     <button onclick="location.href='{% url 'horizon:project:overview:kubernetes_test' %}'">Kubernetes</button>
     {% include "horizon/common/_limit_summary.html" %}
  
     {% if simple_tenant_usage_enabled %}
      {% include "horizon/common/_usage_summary.html" %}
      {{ table.render }}
    {% endif %}
  {% endblock %}
'''
