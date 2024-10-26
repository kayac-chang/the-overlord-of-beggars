import { Form, useLoaderData } from "@remix-run/react";
import {
  useReactTable,
  getCoreRowModel,
  getExpandedRowModel,
  flexRender,
  createColumnHelper,
} from "@tanstack/react-table";
import { ComponentProps, Fragment, ReactNode } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "~/components/ui/table";
import { Toggle } from "~/components/ui/toggle";
import { Store } from "~/models/store";
import { clientLoader } from "./route";
import { LoaderCircle } from "lucide-react";
import { match } from "ts-pattern";

type ExpandButtonProps = {
  value: string;
  pressed: boolean;
  onPressedChange: () => void;
};

function ExpandButton(props: ExpandButtonProps) {
  const data = useLoaderData<typeof clientLoader>();
  const hasLoaded = Boolean(data?.storesWithNearExpiredFoods);

  // 展開點下去瞬間 icon 要變成 loading
  if (props.pressed && hasLoaded) {
    return (
      <Form preventScrollReset>
        <Toggle
          type="submit"
          defaultPressed={props.pressed}
          onPressedChange={props.onPressedChange}
          className="group"
        >
          <span className="group-data-[state=off]:hidden">👇</span>
          <span className="group-data-[state=on]:hidden">
            <LoaderCircle className="size-4 animate-spin" />
          </span>
        </Toggle>

        {data?.query.location && (
          <input type="hidden" name="location" value={data.query.location} />
        )}
        {data?.query.keyword && (
          <input type="hidden" name="keyword" value={data.query.keyword} />
        )}
        {data?.query.stores &&
          data.query.stores
            .filter((store) => store !== props.value)
            .map((store) => (
              <input key={store} type="hidden" name="stores" value={store} />
            ))}
      </Form>
    );
  }

  return (
    <Form preventScrollReset>
      <Toggle
        type="submit"
        defaultPressed={props.pressed}
        onPressedChange={props.onPressedChange}
        name="stores"
        value={props.value}
        className="group"
      >
        <span className="group-data-[state=on]:hidden">👉</span>
        <span className="group-data-[state=off]:hidden">
          <LoaderCircle className="size-4 animate-spin" />
        </span>
      </Toggle>

      {data?.query.location && (
        <input type="hidden" name="location" value={data.query.location} />
      )}
      {data?.query.keyword && (
        <input type="hidden" name="keyword" value={data.query.keyword} />
      )}
      {data?.query.stores &&
        data.query.stores
          .filter((store) => store !== props.value)
          .map((store) => (
            <input key={store} type="hidden" name="stores" value={store} />
          ))}
    </Form>
  );
}

const helper = createColumnHelper<Store>();

const columns = [
  helper.display({
    id: "expand",
    cell: (props) =>
      props.row.getCanExpand() && (
        <ExpandButton
          key={props.row.getIsExpanded() ? "expanded" : "collapsed"}
          pressed={props.row.getIsExpanded()}
          onPressedChange={props.row.toggleExpanded}
          value={props.row.id}
        />
      ),
  }),
  helper.accessor("brand", {
    header: "廠商",
    cell: (props) =>
      match(props.getValue())
        .with("7-11", () => "7-11")
        .with("FamilyMart", () => "全家")
        .exhaustive(),
  }),
  helper.accessor("name", { header: "店名" }),
  helper.accessor("address", { header: "地址" }),
  helper.accessor("distance", {
    header: "距離",
    cell: (props) => {
      const value = props.getValue();

      if (!value) return null;

      return Intl.NumberFormat("zh-TW", {
        style: "unit",
        unit: "meter",
        maximumFractionDigits: 0,
      }).format(value);
    },
  }),
];

type Props = ComponentProps<typeof Table> & {
  data: Store[];
  expanded?: Store["id"][];
  renderSubComponent?: (data: Store) => ReactNode;
};
function StoreTable({ data, renderSubComponent, expanded, ...props }: Props) {
  const table = useReactTable({
    columns,
    data,
    getCoreRowModel: getCoreRowModel(),
    getExpandedRowModel: getExpandedRowModel(),
    getRowId: (row) => row.id,
    getRowCanExpand: () => true,
    state: {
      expanded: expanded?.reduce((acc, id) => {
        return { ...acc, [id]: true };
      }, {} as Record<string, boolean>),
    },
  });

  const head = (
    <TableHeader>
      {table.getHeaderGroups().map((headerGroup) => (
        <TableRow key={headerGroup.id}>
          {headerGroup.headers.map((header) => (
            <TableHead key={header.id} colSpan={header.colSpan}>
              {!header.isPlaceholder &&
                flexRender(header.column.columnDef.header, header.getContext())}
            </TableHead>
          ))}
        </TableRow>
      ))}
    </TableHeader>
  );

  const body = (
    <TableBody>
      {table.getRowModel().rows.map((row) => (
        <Fragment key={row.id}>
          <TableRow>
            {row.getVisibleCells().map((cell) => (
              <TableCell key={cell.id}>
                {flexRender(cell.column.columnDef.cell, cell.getContext())}
              </TableCell>
            ))}
          </TableRow>

          {renderSubComponent && row.getIsExpanded() && (
            <TableRow>
              <TableCell colSpan={row.getVisibleCells().length}>
                {renderSubComponent(row.original)}
              </TableCell>
            </TableRow>
          )}
        </Fragment>
      ))}
    </TableBody>
  );

  return (
    <Table {...props}>
      {head}
      {body}
    </Table>
  );
}

export default StoreTable;
