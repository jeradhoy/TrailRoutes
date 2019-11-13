# Project Proposal

Due Fri. Nov 15th



Description: 

Written proposal (Due Nov 15). You should submit a one page max description of what you would like to pursue for your project. It should clearly state the problem that you are interested in working on and propose some direction for how you are going to go about solving it. References and figures do not count against your 1 page limit.

- Create Trail Routing website
- Frontend that displays trails
    - allows you to find routes (loops between min and max dist, and point-to-point below max) and display options (maybe in sidebar)
    - Mabox map display
    - Sidebar
    - Need vector tile server to serve postgis trails
    - Algorithm can return JSON of edges (or similar) that can be dealt with via highlighting on the frontend
- Redis caching layer for partial routes in algorithm