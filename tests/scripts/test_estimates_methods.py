"""Test script for verifying all Estimate API methods."""
import os
import sys
import time
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from plane.client import PlaneClient
from plane.models.estimates import (
    CreateEstimate,
    CreateEstimatePoint,
    UpdateEstimate,
    UpdateEstimatePoint,
)
from plane.models.projects import CreateProject


def run_test():
    base_url = os.getenv("PLANE_BASE_URL")
    api_key = os.getenv("PLANE_API_KEY")
    access_token = os.getenv("PLANE_ACCESS_TOKEN")
    slug = os.getenv("WORKSPACE_SLUG")

    client = PlaneClient(base_url=base_url, api_key=api_key)

    print("1. Creating Project...")
    project = client.projects.create(
        slug,
        CreateProject(
            name="Estimate API Test",
            identifier=f"EAT{str(int(time.time()))[-4:]}",
        ),
    )
    print(f"   ✅ Project created: {project.name} (ID: {project.id})")

    print("\n2. Creating Estimate...")
    estimate = client.estimates.create(
        slug,
        project.id,
        CreateEstimate(
            name="Complexity Points",
            type="points",
            description="Initial description"
        )
    )
    print(f"   ✅ Estimate created: {estimate.name} (ID: {estimate.id})")

    print("\n3. Retrieving Estimate...")
    retrieved_est = client.estimates.retrieve(slug, project.id)
    print(f"   ✅ Retrieved estimate: {retrieved_est.name} (ID: {retrieved_est.id})")

    print("\n4. Updating Estimate...")
    updated_est = client.estimates.update(
        slug,
        project.id,
        UpdateEstimate(description="Updated description")
    )
    print(f"   ✅ Estimate updated. New description: '{updated_est.description}'")

    print("\n5. Linking Estimate to Project...")
    client.estimates.link_to_project(slug, project.id, estimate.id)
    print("   ✅ Estimate linked successfully to project.")

    print("\n6. Creating Estimate Points...")
    points = client.estimates.create_points(
        slug,
        project.id,
        estimate.id,
        [
            CreateEstimatePoint(value="1", key=0),
            CreateEstimatePoint(value="2", key=1),
            CreateEstimatePoint(value="3", key=2),
        ]
    )
    print(f"   ✅ Created {len(points)} points:")
    for p in points:
        print(f"      - {p.value} (ID: {p.id})")

    point_to_update = points[0]
    point_to_delete = points[1]

    print("\n7. Listing Estimate Points...")
    listed_points = client.estimates.list_points(slug, project.id, estimate.id)
    print(f"   ✅ Listed {len(listed_points)} points.")

    print("\n8. Updating Estimate Point...")
    updated_point = client.estimates.update_point(
        slug,
        project.id,
        estimate.id,
        point_to_update.id,
        UpdateEstimatePoint(value="0.5")
    )
    print(f"   ✅ Point updated from '{point_to_update.value}' to '{updated_point.value}'.")

    print("\n9. Deleting Estimate Point...")
    client.estimates.delete_point(slug, project.id, estimate.id, point_to_delete.id)
    print(f"   ✅ Point '{point_to_delete.value}' deleted successfully.")

    print("\n10. Deleting Estimate...")
    client.estimates.delete(slug, project.id)
    print("   ✅ Estimate deleted successfully.")

    print("\n🎉 All Estimate API methods tested successfully!")


if __name__ == "__main__":
    run_test()
