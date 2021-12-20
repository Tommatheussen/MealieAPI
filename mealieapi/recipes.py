import io
import typing as t
from dataclasses import dataclass, field
from datetime import datetime
from zipfile import ZipFile

from mealieapi.const import YEAR_MONTH_DAY, YEAR_MONTH_DAY_HOUR_MINUTE_SECOND
from mealieapi.misc import name_to_slug
from mealieapi.mixins import JsonModel

if t.TYPE_CHECKING:
    from mealieapi.client import MealieClient


@dataclass()
class RecipeImage(JsonModel):
    _client: "MealieClient" = field(repr=False)
    recipe_slug: str
    image: int


@dataclass()
class RecipeAsset(JsonModel):
    _client: "MealieClient" = field(repr=False)
    recipe_slug: str
    file_name: str
    name: str = None
    icon: str = None

    async def content(self) -> bytes:
        return await self.get_asset(recipe_slug, self.file_name)


@dataclass()
class RecipeComment(JsonModel):
    _client: "MealieClient" = field(repr=False)
    recipt_slug: str
    text: str

    def json(self) -> dict:
        return super().json(
            {
                "text",
            }
        )

    async def update(self, text: str) -> "RecipeComment":
        return await self._client.update_recipe_comment(self.recipe_slug, text)

    async def delete(self) -> None:
        await self._client.delete_recipe_comment(self.recipe_slug, self.text)


@dataclass(repr=False)
class Recipe:
    _client: "MealieClient" = field(repr=False)
    name: str
    description: str = None
    image: str = None
    recipe_yield: str = None
    recipe_ingredient: t.List[str] = None
    recipe_instructions: t.List[t.Dict[str, str]] = None
    tags: t.List[str] = None
    recipe_category: t.List[str] = None
    notes: t.List[t.Dict[str, str]] = None
    rating: int = None
    extras: t.Dict[str, str] = None
    id: int = None
    settings: t.Dict[str, bool] = None
    total_time: str = None
    prep_time: str = None
    perform_time: str = None
    nutrition: t.Dict[str, str] = None
    date_added: datetime = None
    date_updated: datetime = None
    org_url: str = None
    tools: list = None
    assets: list = None
    comments: t.List[RecipeComment] = None

    @property
    def slug(self):
        return name_to_slug(self.name)

    def json(self) -> dict:
        data = super().json(
            {
                "slug",
                "name",
                "description",
                "image",
                "recipe_yield",
                "recipe_ingredient",
                "recipe_instructions",
                "tags",
                "recipe_category",
                "notes",
                "org_url",
                "rating",
                "extras",
                "id",
                "settings",
                "total_time",
                "prep_time",
                "perform_time",
                "nutrition",
                "date_added",
                "date_updated",
                "tools",
                "assets",
                "comments",
            }
        )

        data = {attr: getattr(self, attr) for attr in attrs}
        if data["date_added"]:
            data["date_added"] = data["date_added"].strftime(YEAR_MONTH_DAY)
        if data["date_updated"]:
            data["date_updated"] = data["date_updated"].strftime(YEAR_MONTH_DAY_HOUR_MINUTE_SECOND)
        return data

    async def create(self) -> "Recipe":
        return await self._client.create_recipe(self)

    async def delete(self) -> "Recipe":
        return await self._client.delete_recipe(self.slug)

    async def get_asset(self, file_name: str):
        return await self._client.get_asset(self.slug, file_name)

    async def get_image(self, type="original") -> bytes:
        """
        Gets the image for the recipe.
        Valid types are :code:`original`, :code:`min-original`, and :code:`tiny-original`
        """
        if self.image:
            return await self._client.get_image(self.slug, type)

    async def push_changes(self) -> "Recipe":
        return await self._client.update_recipe(self)

    async def get_zip(self) -> ZipFile:
        return await self._client.get_recipe_zip(self.slug)

    async def refresh(self) -> None:
        recipe = await self._client.get_recipe(self.slug)
        for attr in dir(recipe):
            if not attr.startswith("_"):
                setattr(self, attr, getattr(recipe, attr))

    def __repr__(self):
        return f"<Recipe {self.slug!r}>"


@dataclass()
class RecipeTag:
    _client: "MealieClient" = field(repr=False)
    id: int
    name: str
    recipes: t.List[Recipe] = None

    @property
    def slug(self):
        return name_to_slug(self.name)

    async def update(self, new_name: str) -> None:
        tag = await self._client.update_tag

    async def delete(self):
        pass


@dataclass()
class RecipeCategory:
    _client: "MealieClient" = field(repr=False)
    id: int
    name: str
    recipes: t.List[Recipe] = None

    @property
    def slug(self):
        return name_to_slug(self.name)
