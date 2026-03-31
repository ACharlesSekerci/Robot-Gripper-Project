import trimesh
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import os

sandbox = "/Users/ahmetsekerci/Desktop/Cursor/Robot/sandbox/modified"
output_pdf = "/Users/ahmetsekerci/Desktop/Cursor/Robot/PaperTemplates_v2.pdf"

PAGE_W_MM = 215.9
PAGE_H_MM = 279.4
MARGIN_MM = 15

flat_parts = [
    ("BottomPlate.stl", 1),
    ("TopPlate.stl", 1),
    ("BackPlate.stl", 1),
    ("BackPlateSpacer.stl", 1),
    ("Gear.stl", 1),
    ("LeftFinger.stl", 2),
    ("RightFinger.stl", 2),
    ("FingerTip-Plate.stl", 4),
    ("9GSpacer.stl", 1),
    ("9GSpacer-3mm.stl", 1),
]

cylindrical_parts = [
    ("3mmSpacer.stl", 8),
    ("15mmStandoff.stl", 8),
    ("FingerTip.stl", 2),
]

def draw_part_topdown(ax, mesh, name, qty):
    bounds = mesh.bounds
    dims = bounds[1] - bounds[0]
    mid_z = (bounds[0][2] + bounds[1][2]) / 2
    
    section = mesh.section(plane_origin=[0, 0, mid_z], plane_normal=[0, 0, 1])
    if section is None:
        return False
    path_2d, _ = section.to_planar()
    
    for entity in path_2d.entities:
        pts = path_2d.vertices[entity.points]
        pts_closed = np.vstack([pts, pts[0]])
        ax.plot(pts_closed[:, 0], pts_closed[:, 1], 'k-', linewidth=0.8)
    
    ax.set_aspect('equal')
    pb = path_2d.bounds
    cx = (pb[0][0] + pb[1][0]) / 2
    cy = (pb[0][1] + pb[1][1]) / 2
    aw = PAGE_W_MM - 2 * MARGIN_MM
    ah = PAGE_H_MM - 2 * MARGIN_MM - 30
    ax.set_xlim(cx - aw/2, cx + aw/2)
    ax.set_ylim(cy - ah/2, cy + ah/2)
    
    ax.set_title(f"{name}  |  Qty: {qty}x  |  {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm  |  TOP VIEW\n1:1 SCALE", fontsize=11, fontweight='bold', pad=15)
    
    bar_x = cx + aw/2 - 25
    bar_y = cy - ah/2 + 10
    ax.plot([bar_x, bar_x + 10], [bar_y, bar_y], 'r-', linewidth=3)
    ax.text(bar_x + 5, bar_y + 2, '10mm', ha='center', fontsize=8, color='red')
    ax.grid(True, alpha=0.15)
    return True


def draw_part_side(ax, mesh, name, qty):
    bounds = mesh.bounds
    dims = bounds[1] - bounds[0]
    
    verts = mesh.vertices
    
    # Create a proper side profile by projecting to XZ
    # Collect boundary edges visible from side
    x_vals = verts[:, 0]
    z_vals = verts[:, 2]
    
    # Use convex hull of XZ projection for clean outline
    from scipy.spatial import ConvexHull
    points_xz = np.column_stack([x_vals, z_vals])
    
    try:
        hull = ConvexHull(points_xz)
        hull_pts = points_xz[hull.vertices]
        hull_pts = np.vstack([hull_pts, hull_pts[0]])
        ax.plot(hull_pts[:, 0], hull_pts[:, 1], 'k-', linewidth=1.0)
        ax.fill(hull_pts[:, 0], hull_pts[:, 1], alpha=0.05, color='gray')
    except:
        ax.scatter(points_xz[:, 0], points_xz[:, 1], s=0.5, c='k')
    
    # Also try to show the center hole if it exists
    mid_y = (bounds[0][1] + bounds[1][1]) / 2
    try:
        section = mesh.section(plane_origin=[0, mid_y, 0], plane_normal=[0, 1, 0])
        if section is not None:
            path_2d, _ = section.to_planar()
            for entity in path_2d.entities:
                pts = path_2d.vertices[entity.points]
                pts_closed = np.vstack([pts, pts[0]])
                ax.plot(pts_closed[:, 0], pts_closed[:, 1], 'k-', linewidth=0.8)
    except:
        pass
    
    ax.set_aspect('equal')
    
    cx = (bounds[0][0] + bounds[1][0]) / 2
    cz = (bounds[0][2] + bounds[1][2]) / 2
    aw = PAGE_W_MM - 2 * MARGIN_MM
    ah = PAGE_H_MM - 2 * MARGIN_MM - 30
    ax.set_xlim(cx - aw/2, cx + aw/2)
    ax.set_ylim(cz - ah/2, cz + ah/2)
    
    ax.set_title(f"{name}  |  Qty: {qty}x  |  {dims[0]:.1f} x {dims[1]:.1f} x {dims[2]:.1f} mm  |  SIDE VIEW\n1:1 SCALE - height is vertical", fontsize=11, fontweight='bold', pad=15)
    
    bar_x = cx + aw/2 - 25
    bar_y = cz - ah/2 + 10
    ax.plot([bar_x, bar_x + 10], [bar_y, bar_y], 'r-', linewidth=3)
    ax.text(bar_x + 5, bar_y + 2, '10mm', ha='center', fontsize=8, color='red')
    ax.grid(True, alpha=0.15)
    ax.set_xlabel('mm (width)')
    ax.set_ylabel('mm (height)')
    return True


fig_w = PAGE_W_MM / 25.4
fig_h = PAGE_H_MM / 25.4

with PdfPages(output_pdf) as pdf:
    for fname, qty in flat_parts:
        mesh = trimesh.load(os.path.join(sandbox, fname))
        fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h))
        name = fname.replace('.stl', '')
        if draw_part_topdown(ax, mesh, name, qty):
            plt.tight_layout()
            pdf.savefig(fig)
            print(f"  TOP VIEW: {name} x{qty}")
        plt.close(fig)
    
    for fname, qty in cylindrical_parts:
        mesh = trimesh.load(os.path.join(sandbox, fname))
        fig, ax = plt.subplots(1, 1, figsize=(fig_w, fig_h))
        name = fname.replace('.stl', '')
        if draw_part_side(ax, mesh, name, qty):
            plt.tight_layout()
            pdf.savefig(fig)
            print(f"  SIDE VIEW: {name} x{qty}")
        plt.close(fig)

print(f"\nDone! Saved: {output_pdf}")
